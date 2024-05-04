from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    health_records = db.relationship('HealthRecord', back_populates='user', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class HealthRecord(db.Model):
    __tablename__ = 'health_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    blood_pressure_systolic = db.Column(db.Integer, nullable=False)
    blood_pressure_diastolic = db.Column(db.Integer, nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', back_populates='health_records')
    values = db.relationship('HealthRecordValue', back_populates='health_record', cascade="all, delete-orphan")


class HealthMetric(db.Model):
    __tablename__ = 'health_metrics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    health_record_values = db.relationship('HealthRecordValue', back_populates='metric', cascade="all, delete-orphan")


class HealthRecordValue(db.Model):
    __tablename__ = 'health_record_values'
    id = db.Column(db.Integer, primary_key=True)
    health_record_id = db.Column(db.Integer, db.ForeignKey('health_records.id'), nullable=False)
    metric_id = db.Column(db.Integer, db.ForeignKey('health_metrics.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    health_record = db.relationship('HealthRecord', back_populates='values')
    metric = db.relationship('HealthMetric', back_populates='health_record_values')
