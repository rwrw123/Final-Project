import unittest
from flask_testing import TestCase
from app import create_app, db

class TestApp(TestCase):  # Ensure the class name starts with 'Test'
    def create_app(self):
        app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Health Monitoring System', response.data)

if __name__ == '__main__':
    unittest.main()






