import datetime
from app import create_app, db
from app.models import User, HealthMetric, HealthRecord, HealthRecordValue

app = create_app()

with app.app_context():
    db.create_all()

    # Seed the database with initial data
    if not User.query.first():
        user = User(username="admin", email="admin@example.com", role="admin")
        user.set_password("password")
        db.session.add(user)

        metric = HealthMetric(name="Weight", unit="kg")
        db.session.add(metric)

        record = HealthRecord(user=user, timestamp=datetime.datetime.now())
        db.session.add(record)

        record_value = HealthRecordValue(record=record, metric=metric, value=70.0)
        db.session.add(record_value)

        db.session.commit()

    # Output the seeded data
    print(User.query.all())
    print(HealthMetric.query.all())
    print(HealthRecord.query.all())
    print(HealthRecordValue.query.all())
















