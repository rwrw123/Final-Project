from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class HealthMetric(db.Model):
    __tablename__ = 'health_metrics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    unit = db.Column(db.String(64), nullable=False)

class HealthRecord(db.Model):
    __tablename__ = 'health_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    health_metric_id = db.Column(db.Integer, db.ForeignKey('health_metrics.id'))
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class HealthRecordValue(db.Model):
    __tablename__ = 'health_record_values'
    id = db.Column(db.Integer, primary_key=True)
    health_record_id = db.Column(db.Integer, db.ForeignKey('health_records.id'))
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


