from app import create_app, db
from app.models import User, HealthMetric, HealthRecord, HealthRecordValue

# Create an app context
app = create_app()
with app.app_context():
    # Recreate the tables
    db.create_all()

    # Add a test user if none exists
    if not User.query.first():
        user = User(username="testuser", email="testuser@example.com", role="user")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        # Add a test health metric
        metric = HealthMetric(name="Weight", unit="kg")
        db.session.add(metric)
        db.session.commit()

        # Add a test health record for the user and metric
        record = HealthRecord(user_id=user.id, health_metric_id=metric.id, value=70.5)
        db.session.add(record)
        db.session.commit()

        # Add a test health record value
        record_value = HealthRecordValue(health_record_id=record.id, value=70.5)
        db.session.add(record_value)
        db.session.commit()








