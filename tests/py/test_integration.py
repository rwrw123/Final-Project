import unittest
from flask_testing import TestCase
from app import create_app, db

class TestIntegration(TestCase):  # Ensure the class name starts with 'Test'
    def create_app(self):
        app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation(self):
        from app.models import User
        user = User(username='testuser', email='testuser@example.com', password_hash='testpassword')
        db.session.add(user)
        db.session.commit()
        result = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(result)

    def test_metric_creation(self):
        from app.models import HealthMetric
        metric = HealthMetric(name='Weight', unit='kg')
        db.session.add(metric)
        db.session.commit()
        result = HealthMetric.query.filter_by(name='Weight'). first()
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()



