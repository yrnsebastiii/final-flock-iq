# flock_models.py - COMPLETE REVISION
from db_ext import db
from datetime import datetime, date
import json

# ─────────────────────────────────────────────────────────────────────────
# flock_user
# ─────────────────────────────────────────────────────────────────────────
class User(db.Model):
    __tablename__ = 'flock_user'
    user_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    phone_num = db.Column(db.String(20))
    address = db.Column(db.String(200))
    bday = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Owner, Manager, Worker
    is_active = db.Column(db.Boolean, default=True)

    @property
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(p for p in parts if p)

    @property
    def age(self):
        if not self.bday:
            return None
        today = date.today()
        return today.year - self.bday.year - ((today.month, today.day) < (self.bday.month, self.bday.day))

# ─────────────────────────────────────────────────────────────────────────
# flock_batch
# ─────────────────────────────────────────────────────────────────────────
class FlockBatch(db.Model):
    __tablename__ = 'flock_batch'
    batch_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    batch_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, default=date.today)
    target_harvest_date = db.Column(db.Date)
    initial_bird_count = db.Column(db.Integer, default=0)
    current_bird_count = db.Column(db.Integer, default=0)
    flock_status = db.Column(db.String(20), default='Active')  # Active, Harvested, Archived
    budget_allocated = db.Column(db.Float, default=0.0)
    season = db.Column(db.String(20))  # Dry, Wet

    creator = db.relationship('User', foreign_keys=[user_id])

    @property
    def age_days(self):
        return max(0, (date.today() - self.start_date).days)

    @property
    def target_age_days(self):
        """Days from start to target harvest date."""
        if self.target_harvest_date and self.start_date:
            return max(1, (self.target_harvest_date - self.start_date).days)
        return 35

    @property
    def mortality_count(self):
        return max(0, self.initial_bird_count - self.current_bird_count)

    @property
    def mortality_percentage(self):
        if self.initial_bird_count > 0:
            return round((self.mortality_count / self.initial_bird_count) * 100, 2)
        return 0.0

    @property
    def has_data(self):
        return bool(
            MortalityRecord.query.filter_by(batch_id=self.batch_id).first()
            or WeightRecord.query.filter_by(batch_id=self.batch_id).first()
            or DailyFeedRecord.query.filter_by(batch_id=self.batch_id).first()
            or HarvestSale.query.filter_by(batch_id=self.batch_id).first()
        )

# ─────────────────────────────────────────────────────────────────────────
# Vaccine / VaccinationRecord
# ─────────────────────────────────────────────────────────────────────────
class Vaccine(db.Model):
    __tablename__ = 'vaccine'
    vaccine_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    vaccine_name = db.Column(db.String(100), nullable=False)
    vaccine_type = db.Column(db.String(50))
    vaccine_exp_date = db.Column(db.Date)
    milliliters_per_bottle = db.Column(db.Float, default=0.0)
    remaining_quantity = db.Column(db.Float, default=0.0)

class VaccinationRecord(db.Model):
    __tablename__ = 'vaccination_record'
    vaccination_record_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=False)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.vaccine_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    dose_per_bird = db.Column(db.Float, default=0.0)
    administered_by = db.Column(db.String(100))
    scheduled_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Scheduled')

    batch = db.relationship('FlockBatch', backref=db.backref('vaccinations', cascade='all, delete-orphan'))
    vaccine = db.relationship('Vaccine', backref='vaccination_records')

# ─────────────────────────────────────────────────────────────────────────
# Vitamin / VitaminSchedule
# ─────────────────────────────────────────────────────────────────────────
class Vitamin(db.Model):
    __tablename__ = 'vitamin'
    vitamin_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    vitamin_name = db.Column(db.String(100), nullable=False)
    vitamin_type = db.Column(db.String(50))
    vitamin_exp_date = db.Column(db.Date)
    quantity = db.Column(db.Float, default=0.0)
    unit = db.Column(db.String(20))

class Medicine(db.Model):
    __tablename__ = 'medicine'
    medicine_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    medicine_name = db.Column(db.String(100), nullable=False)
    medicine_type = db.Column(db.String(50))
    medicine_exp_date = db.Column(db.Date)
    quantity = db.Column(db.Float, default=0.0)
    unit = db.Column(db.String(20))

class VitaminSchedule(db.Model):
    __tablename__ = 'vitamin_schedule'
    schedule_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=False)
    vitamin_id = db.Column(db.Integer, db.ForeignKey('vitamin.vitamin_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    day_given = db.Column(db.Integer, nullable=False)
    dosage = db.Column(db.String(50))
    scheduled_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Scheduled')
    administered_by = db.Column(db.String(100))
    cost = db.Column(db.Float, default=0.0)
    quantity_used = db.Column(db.Float, default=0.0)

    batch = db.relationship('FlockBatch', backref=db.backref('vitamin_schedules', cascade='all, delete-orphan'))
    vitamin = db.relationship('Vitamin', backref='schedules')

# ─────────────────────────────────────────────────────────────────────────
# MedicationSchedule
# ─────────────────────────────────────────────────────────────────────────
class MedicationSchedule(db.Model):
    __tablename__ = 'medication_schedule'
    schedule_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    item_type = db.Column(db.String(20), default='Medicine')
    dosage = db.Column(db.String(50))
    scheduled_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Scheduled')
    administered_by = db.Column(db.String(100))
    notes = db.Column(db.Text)
    cost = db.Column(db.Float, default=0.0)
    quantity_used = db.Column(db.Float, default=0.0)

    batch = db.relationship('FlockBatch', backref=db.backref('medication_schedules', cascade='all, delete-orphan'))

# ─────────────────────────────────────────────────────────────────────────
# MortalityRecord, WeightRecord, ADG/FCR
# ─────────────────────────────────────────────────────────────────────────
class MortalityRecord(db.Model):
    __tablename__ = 'mortality_record'
    mortality_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    death_count = db.Column(db.Integer, default=0)
    cull_count = db.Column(db.Integer, default=0)
    cause = db.Column(db.String(200))
    record_date = db.Column(db.Date, default=date.today)

    batch = db.relationship('FlockBatch', backref=db.backref('mortality_records', cascade='all, delete-orphan'))

class WeightRecord(db.Model):
    __tablename__ = 'weight_record'
    weight_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    record_date = db.Column(db.Date, default=date.today)
    total_weight_gain = db.Column(db.Float, default=0.0)
    fcr_value = db.Column(db.Float, default=0.0)

    batch = db.relationship('FlockBatch', backref=db.backref('weight_records', cascade='all, delete-orphan'))
    user = db.relationship('User', foreign_keys=[user_id])

class AdgCalculation(db.Model):
    __tablename__ = 'adg_calculation'
    calc_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    starting_weight = db.Column(db.Float, default=0.0)
    ending_weight = db.Column(db.Float, default=0.0)
    number_of_days = db.Column(db.Integer, default=0)
    record_date = db.Column(db.Date, default=date.today)
    adg_value = db.Column(db.Float, default=0.0)

    batch = db.relationship('FlockBatch', backref=db.backref('adg_calculations', cascade='all, delete-orphan'))

class FcrCalculation(db.Model):
    __tablename__ = 'fcr_calculation'
    fcr_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    total_feed_intake = db.Column(db.Float, default=0.0)
    total_weight_gain = db.Column(db.Float, default=0.0)
    fcr_value = db.Column(db.Float, default=0.0)

    batch = db.relationship('FlockBatch', backref=db.backref('fcr_calculations', cascade='all, delete-orphan'))

class FlockReport(db.Model):
    __tablename__ = 'flock_report'
    report_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    adg_id = db.Column(db.Integer, db.ForeignKey('adg_calculation.calc_id'), nullable=False)
    fcr_id = db.Column(db.Integer, db.ForeignKey('fcr_calculation.fcr_id'), nullable=False)
    report_date = db.Column(db.Date, default=date.today)

    batch = db.relationship('FlockBatch', backref=db.backref('reports', cascade='all, delete-orphan'))
    adg = db.relationship('AdgCalculation')
    fcr = db.relationship('FcrCalculation')

# ─────────────────────────────────────────────────────────────────────────
# WeeklyRecord
# ─────────────────────────────────────────────────────────────────────────
class WeeklyRecord(db.Model):
    __tablename__ = 'weekly_record'
    weekly_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    total_weight_sample = db.Column(db.Float, default=0.0)
    total_birds_weighed = db.Column(db.Integer, default=0)
    avg_bird_weight = db.Column(db.Float, default=0.0)
    record_date = db.Column(db.Date, default=date.today)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')

    batch = db.relationship('FlockBatch', backref=db.backref('weekly_records', cascade='all, delete-orphan'))
    worker = db.relationship('User', foreign_keys=[user_id])

# ─────────────────────────────────────────────────────────────────────────
# MarketPrice
# ─────────────────────────────────────────────────────────────────────────
class MarketPrice(db.Model):
    __tablename__ = 'market_price'
    price_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    record_date = db.Column(db.Date, default=date.today)
    price_per_kg = db.Column(db.Float, default=0.0)
    location = db.Column(db.String(100))

# ─────────────────────────────────────────────────────────────────────────
# FeedRecord / DailyFeedRecord
# ─────────────────────────────────────────────────────────────────────────
class FeedRecord(db.Model):
    __tablename__ = 'feed_record'
    feed_record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    feed_name = db.Column(db.String(100), nullable=False)
    feed_category = db.Column(db.String(50), default='Chick Booster')
    expiration_date = db.Column(db.Date)
    season = db.Column(db.String(20))
    crude_protein = db.Column(db.Float, default=0.0)
    crude_fat = db.Column(db.Float, default=0.0)
    crude_fiber = db.Column(db.Float, default=0.0)
    moisture = db.Column(db.Float, default=0.0)
    calcium = db.Column(db.Float, default=0.0)
    phosphorus = db.Column(db.Float, default=0.0)
    remaining_quantity = db.Column(db.Float, default=0.0)

class DailyFeedRecord(db.Model):
    __tablename__ = 'daily_feed_record'
    daily_feed_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=False)
    feed_record_id = db.Column(db.Integer, db.ForeignKey('feed_record.feed_record_id'), nullable=False)
    record_date = db.Column(db.Date, default=date.today)
    total_kg = db.Column(db.Float, default=0.0)

    batch = db.relationship('FlockBatch', backref=db.backref('daily_feed_records', cascade='all, delete-orphan'))
    feed = db.relationship('FeedRecord')

# ─────────────────────────────────────────────────────────────────────────
# Expense tables
# ─────────────────────────────────────────────────────────────────────────
class ExpenseCategory(db.Model):
    __tablename__ = 'expense_category'
    expense_category_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    category_name = db.Column(db.String(100), nullable=False)

class WaterExpense(db.Model):
    __tablename__ = 'water_expense'
    expense_id = db.Column(db.Integer, primary_key=True)
    expense_category_id = db.Column(db.Integer, db.ForeignKey('expense_category.expense_category_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=True)
    water_expense_amount = db.Column(db.Float, default=0.0)
    water_expense_status = db.Column(db.String(20), default='Pending')
    expense_date = db.Column(db.Date, default=date.today)

    category = db.relationship('ExpenseCategory', backref=db.backref('water_expenses', cascade='all, delete-orphan'))
    batch = db.relationship('FlockBatch', backref=db.backref('water_expenses', cascade='all, delete-orphan'))

class ElectricityExpense(db.Model):
    __tablename__ = 'electricity_expense'
    expense_id = db.Column(db.Integer, primary_key=True)
    expense_category_id = db.Column(db.Integer, db.ForeignKey('expense_category.expense_category_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=True)
    electricity_expense_amount = db.Column(db.Float, default=0.0)
    electricity_expense_status = db.Column(db.String(20), default='Pending')
    expense_date = db.Column(db.Date, default=date.today)

    category = db.relationship('ExpenseCategory', backref=db.backref('electricity_expenses', cascade='all, delete-orphan'))
    batch = db.relationship('FlockBatch', backref=db.backref('electricity_expenses', cascade='all, delete-orphan'))

class LpgExpense(db.Model):
    __tablename__ = 'lpg_expense'
    expense_id = db.Column(db.Integer, primary_key=True)
    expense_category_id = db.Column(db.Integer, db.ForeignKey('expense_category.expense_category_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=True)
    lpg_expense_amount = db.Column(db.Float, default=0.0)
    lpg_provider = db.Column(db.String(100))
    lpg_expense_status = db.Column(db.String(20), default='Pending')
    expense_date = db.Column(db.Date, default=date.today)

    category = db.relationship('ExpenseCategory', backref=db.backref('lpg_expenses', cascade='all, delete-orphan'))
    batch = db.relationship('FlockBatch', backref=db.backref('lpg_expenses', cascade='all, delete-orphan'))

class LaborExpense(db.Model):
    __tablename__ = 'labor_expense'
    expense_id = db.Column(db.Integer, primary_key=True)
    expense_category_id = db.Column(db.Integer, db.ForeignKey('expense_category.expense_category_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=True)
    labor_expense_amount = db.Column(db.Float, default=0.0)
    labor_expense_status = db.Column(db.String(20), default='Pending')
    expense_date = db.Column(db.Date, default=date.today)

    category = db.relationship('ExpenseCategory', backref=db.backref('labor_expenses', cascade='all, delete-orphan'))
    batch = db.relationship('FlockBatch', backref=db.backref('labor_expenses', cascade='all, delete-orphan'))

class OtherExpense(db.Model):
    __tablename__ = 'other_expense'
    expense_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    expense_category_id = db.Column(db.Integer, db.ForeignKey('expense_category.expense_category_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=True)
    other_expense_amount = db.Column(db.Float, default=0.0)
    other_expense_status = db.Column(db.String(20), default='Pending')
    expense_date = db.Column(db.Date, default=date.today)

    category = db.relationship('ExpenseCategory', backref=db.backref('other_expenses', cascade='all, delete-orphan'))
    batch = db.relationship('FlockBatch', backref=db.backref('other_expenses', cascade='all, delete-orphan'))

class VaccineExpense(db.Model):
    __tablename__ = 'vaccine_expense'
    expense_id = db.Column(db.Integer, primary_key=True)
    vaccine_id = db.Column(db.Integer, db.ForeignKey('vaccine.vaccine_id'), nullable=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=True)
    vaccine_expense_amount = db.Column(db.Float, default=0.0)
    vaccine_expense_status = db.Column(db.String(20), default='Pending')
    expense_date = db.Column(db.Date, default=date.today)
    description = db.Column(db.String(200))

    batch = db.relationship('FlockBatch', backref=db.backref('vaccine_expenses', cascade='all, delete-orphan'))

class ChickExpense(db.Model):
    __tablename__ = 'chick_expense'
    expense_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=True)
    quantity = db.Column(db.Integer, default=0)
    chick_expense_amount = db.Column(db.Float, default=0.0)
    chick_expense_status = db.Column(db.String(20), default='Paid')
    expense_date = db.Column(db.Date, default=date.today)
    description = db.Column(db.String(200))

    batch = db.relationship('FlockBatch', backref=db.backref('chick_expenses', cascade='all, delete-orphan'))

class FeedExpense(db.Model):
    __tablename__ = 'feed_expense'
    expense_id = db.Column(db.Integer, primary_key=True)
    feed_record_id = db.Column(db.Integer, db.ForeignKey('feed_record.feed_record_id'), nullable=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=True)
    feed_expense_amount = db.Column(db.Float, default=0.0)
    feed_expense_status = db.Column(db.String(20), default='Pending')
    expense_date = db.Column(db.Date, default=date.today)
    description = db.Column(db.String(200))

    batch = db.relationship('FlockBatch', backref=db.backref('feed_expenses', cascade='all, delete-orphan'))

# ─────────────────────────────────────────────────────────────────────────
# HarvestHistory
# ─────────────────────────────────────────────────────────────────────────
class HarvestHistory(db.Model):
    __tablename__ = 'harvest_history'
    id = db.Column(db.Integer, primary_key=True)
    batch_name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, default=0)
    initial_count = db.Column(db.Integer, default=0)
    harvest_count = db.Column(db.Integer, default=0)
    mortality_pct = db.Column(db.Float, default=0.0)
    total_deaths = db.Column(db.Integer, default=0)
    culled = db.Column(db.Integer, default=0)
    adg = db.Column(db.Float, default=0.0)
    fcr = db.Column(db.Float, default=0.0)
    lw = db.Column(db.Float, default=0.0)
    expenses = db.Column(db.Float, default=0.0)
    season = db.Column(db.String(20))
    chick_booster = db.Column(db.String(50))
    grower_pellets = db.Column(db.String(50))
    finisher_pellets = db.Column(db.String(50))
    vaccine_day_12 = db.Column(db.String(100))
    vaccine_day_16 = db.Column(db.String(100))
    medicines = db.Column(db.String(200))
    budget_allocated = db.Column(db.Float, default=0.0)
    loss_gain = db.Column(db.Float, default=0.0)
    remarks = db.Column(db.String(200))
    is_archived = db.Column(db.Boolean, default=False)
    price_basis = db.Column(db.String(20), default='DA')
    price_basis_value = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ─────────────────────────────────────────────────────────────────────────
# DailyRecordSubmission
# ─────────────────────────────────────────────────────────────────────────
class DailyRecordSubmission(db.Model):
    __tablename__ = 'daily_record_submission'
    submission_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    record_date = db.Column(db.Date, nullable=False, default=date.today)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    avg_weight_g = db.Column(db.Float, default=0.0)
    mortality = db.Column(db.Integer, default=0)
    cull = db.Column(db.Integer, default=0)
    cause = db.Column(db.String(200))
    feed_kg = db.Column(db.Float, default=0.0)
    feed_record_id = db.Column(db.Integer, db.ForeignKey('feed_record.feed_record_id'), nullable=True)

    status = db.Column(db.String(20), default='Pending')
    reviewed_by = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=True)
    reviewed_at = db.Column(db.DateTime)
    review_notes = db.Column(db.String(300))

    batch = db.relationship('FlockBatch', backref=db.backref('submissions', cascade='all, delete-orphan'))
    worker = db.relationship('User', foreign_keys=[user_id])
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    feed = db.relationship('FeedRecord')

# ─────────────────────────────────────────────────────────────────────────
# HarvestSale
# ─────────────────────────────────────────────────────────────────────────
class HarvestSale(db.Model):
    __tablename__ = 'harvest_sale'
    sale_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    sale_date = db.Column(db.Date, default=date.today)
    kg_sold = db.Column(db.Float, default=0.0)
    price_per_kg = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    buyer = db.Column(db.String(100))
    remarks = db.Column(db.String(200))

    batch = db.relationship('FlockBatch', backref=db.backref('sales', cascade='all, delete-orphan'))
    seller = db.relationship('User', foreign_keys=[user_id])

# ─────────────────────────────────────────────────────────────────────────
# PerformanceReport
# ─────────────────────────────────────────────────────────────────────────
class PerformanceReport(db.Model):
    __tablename__ = 'performance_report'
    report_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('flock_user.user_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('flock_batch.batch_id'), nullable=True)
    farm_name = db.Column(db.String(100))
    harvest_month = db.Column(db.String(50))
    data_json = db.Column(db.Text, nullable=False, default='{}')
    farm_head_name = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Submitted')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship('User', foreign_keys=[user_id])
    batch = db.relationship('FlockBatch')