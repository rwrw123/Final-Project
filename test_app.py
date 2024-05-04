import unittest
from flask_testing import TestCase
from app import create_app, db
from app.models import User, HealthRecord
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session

class BaseTestCase(TestCase):
    def create_app(self):
        return create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'SECRET_KEY': 'v9C5OIo8V8Bf1PViyC3Dtw'
        })

    def setUp(self):
        db.create_all()
        session_obj = Session(bind=db.engine)
        hashed_password = generate_password_hash('testpassword')
        user = User(username='testuser', password=hashed_password)
        session_obj.add(user)
        session_obj.commit()
        session_obj.close()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_registration_and_login(self):
        with self.client:
            response = self.client.post('/register', data={
                'username': 'newuser',
                'password': 'newpassword'
            }, follow_redirects=True)
            self.assertIn(b'Login', response.data)

            response = self.client.post('/login', data={
                'username': 'newuser',
                'password': 'newpassword'
            }, follow_redirects=True)
            self.assertIn(b'Dashboard', response.data)

if __name__ == '__main__':
    unittest.main()


