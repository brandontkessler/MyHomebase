import unittest
from flask import current_app
from app import create_app, db
from app.models import User


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(email='test@gmail.com', password="cat")
        self.assertFalse(u.verify_password('dog'))
        self.assertTrue(u.verify_password('cat'))

    def test_random_salts(self):
        u = User(email='test@gmail.com', password="cat")
        u2 = User(email='test2@gmail.com', password="cat")
        self.assertFalse(u.password_hash == u2.password_hash)
