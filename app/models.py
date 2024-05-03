from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_doctor = db.Column(db.Boolean, default=False)

class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    blood_pressure = db.Column(db.String(50), nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('records', lazy=True))
