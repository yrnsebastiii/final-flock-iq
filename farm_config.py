import os

class Config:
    SECRET_KEY = "poultry-farm-secret-key-v1"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/poultry_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'static/uploads'

if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)