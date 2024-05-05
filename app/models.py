import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    health_records = db.relationship('HealthRecord', back_populates='user', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class HealthMetric(db.Model):
    __tablename__ = 'health_metrics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    unit = db.Column(db.String(64), nullable=False)
    health_record_values = db.relationship('HealthRecordValue', back_populates='metric', cascade="all, delete-orphan")


class HealthRecord(db.Model):
    __tablename__ = 'health_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    health_record_values = db.relationship('HealthRecordValue', back_populates='record', cascade="all, delete-orphan")

    user = db.relationship('User', back_populates='health_records')


class HealthRecordValue(db.Model):
    __tablename__ = 'health_record_values'
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('health_records.id'), nullable=False)
    metric_id = db.Column(db.Integer, db.ForeignKey('health_metrics.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)

    record = db.relationship('HealthRecord', back_populates='health_record_values')
    metric = db.relationship('HealthMetric', back_populates='health_record_values')


if __name__ == "__main__":
    from . import create_app
    app = create_app()
    with app.app_context():
        print(User.query.all())
        print(HealthMetric.query.all())
        print(HealthRecord.query.all())
        print(HealthRecordValue.query.all())





















