# setup_db.py
from app import create_app, db
from app.models import User, HealthRecord, HealthMetric, HealthRecordValue
from datetime import date

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()

    # Check if there are any users in the database
    if not User.query.first():  
        user1 = User(username='user1', email='user1@example.com', role='user')
        user1.set_password('password1')
        user2 = User(username='admin', email='admin@example.com', role='admin')
        user2.set_password('admin')

        temp_metric = HealthMetric(name='Temperature', unit='°C')
        bp_metric = HealthMetric(name='Blood Pressure Systolic', unit='mmHg')
        hr_metric = HealthMetric(name='Heart Rate', unit='bpm')
        db.session.add_all([temp_metric, bp_metric, hr_metric])

        record1 = HealthRecord(user=user1, temperature=98.6, blood_pressure_systolic=120, blood_pressure_diastolic=80, heart_rate=72)
        record2 = HealthRecord(user=user2, temperature=99.1, blood_pressure_systolic=110, blood_pressure_diastolic=70, heart_rate=80)

        db.session.add_all([user1, user2, record1, record2])
        db.session.commit()

    print("Database setup complete with initial data.")
