import unittest
from app import create_app, db
from app.models import User
from flask_testing import TestCase

class TestUserManagement(TestCase):

    def create_app(self):
        """Create a test app."""
        app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        return app

    def setUp(self):
        """Set up the test database."""
        db.create_all()
        user = User(username="testuser", email="testuser@example.com", role="user")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """Tear down the test database."""
        db.session.remove()
        db.drop_all()

    def test_register_and_login(self):
        """Test user registration and login."""
        response = self.client.post('/register', data={
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password': 'password',
            'confirm_password': 'password'
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/login', data={
            'username': 'testuser2',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_dashboard(self):
        """Test dashboard access after login."""
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_submit_health_record(self):
        """Test submitting a health record."""
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/submit_record', data={
            'temperature': '98.6',
            'blood_pressure_systolic': '120',
            'blood_pressure_diastolic': '80',
            'heart_rate': '72'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Health record added successfully', response.data)



