from flask import Flask
from farm_config import Config
from db_ext import db
from flock_models import User, HarvestHistory
from flock_routes import bp
from werkzeug.security import generate_password_hash
from datetime import date
from sqlalchemy import func

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        ensure_owner()
        app.register_blueprint(bp)

        @app.context_processor
        def inject_harvest_years():
            years = db.session.query(
                func.extract('year', HarvestHistory.end_date).label('year')
            ).distinct().order_by(
                func.extract('year', HarvestHistory.end_date).desc()
            ).all()
            return dict(harvest_years=[int(y.year) for y in years if y.year])

    return app

def ensure_owner():
    if not User.query.filter_by(username="owner").first():
        db.session.add(User(
            username="owner",
            password_hash=generate_password_hash("owner123"),
            role="Owner",
            first_name="Farm",
            last_name="Owner",
        ))
        db.session.commit()

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)