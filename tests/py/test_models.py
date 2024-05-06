import unittest
import datetime
from flask_testing import TestCase
from app import create_app, db
from app.models import User, HealthMetric, HealthRecord, HealthRecordValue

class TestUserModel(TestCase): 
    def create_app(self):
        app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_health_record(self):
        user = User(username='testuser', email='testuser@example.com', password_hash='testpassword')
        db.session.add(user)
        db.session.commit()
        record = HealthRecord(user=user, timestamp=datetime.datetime.now())
        db.session.add(record)
        db.session.commit()
        result = HealthRecord.query.filter_by(user=user).first()
        self.assertIsNotNone(result)

    def test_set_password(self):
        user = User(username='testuser', email='testuser@example.com')
        user.set_password('password')
        self.assertTrue(user.check_password('password'))

class TestHealthMetricModel(TestCase):  
    def create_app(self):
        app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_health_metric(self):
        metric = HealthMetric(name='Weight', unit='kg')
        db.session.add(metric)
        db.session.commit()
        result = HealthMetric.query.filter_by(name='Weight').first()
        self.assertIsNotNone(result)

class TestHealthRecordValueModel(TestCase):  
    def create_app(self):
        app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_health_record_value(self):
        metric = HealthMetric(name='Weight', unit='kg')
        db.session.add(metric)
        user = User(username='testuser', email='testuser@example.com', password_hash='testpassword')
        db.session.add(user)
        record = HealthRecord(user=user, timestamp=datetime.datetime.now())
        db.session.add(record)
        db.session.commit()
        value = HealthRecordValue(record=record, metric=metric, value=70)
        db.session.add(value)
        db.session.commit()
        result = HealthRecordValue.query.filter_by(value=70).first()
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()









