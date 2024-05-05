import unittest
from app import create_app, db
from app.models import User, HealthMetric, HealthRecord, HealthRecordValue
from datetime import datetime


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        user = User(username="testuser", email="testuser@example.com", role="user")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_health_record(self):
        user = User.query.first()
        record = HealthRecord(user_id=user.id, date=datetime.now())
        db.session.add(record)
        db.session.commit()
        self.assertIsNotNone(record.id)

    def test_set_password(self):
        user = User.query.first()
        user.set_password("newpassword")
        db.session.commit()
        self.assertTrue(user.check_password("newpassword"))


class TestHealthMetricModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        metric = HealthMetric(name="Weight", unit="kg")
        db.session.add(metric)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_health_metric(self):
        metric = HealthMetric(name="Height", unit="cm")
        db.session.add(metric)
        db.session.commit()
        self.assertIsNotNone(metric.id)


class TestHealthRecordValueModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        user = User(username="testuser", email="testuser@example.com", role="user")
        user.set_password("password")
        db.session.add(user)
        metric = HealthMetric(name="Weight", unit="kg")
        db.session.add(metric)
        record = HealthRecord(user=user, date=datetime.now())
        db.session.add(record)
        db.session.commit()
        value = HealthRecordValue(record_id=record.id, metric_id=metric.id, value=70)
        db.session.add(value)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_health_record_value(self):
        record_value = HealthRecordValue.query.first()
        self.assertIsNotNone(record_value.id)


if __name__ == "__main__":
    unittest.main()






