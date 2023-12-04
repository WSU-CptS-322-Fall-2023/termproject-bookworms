import warnings
warnings.filterwarnings("ignore")
import os
basedir = os.path.abspath(os.path.dirname(__file__))

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.Model.models import Admin, User, Book, Review
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ROOT_PATH = '..//'+basedir
    
class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='ben', email='ben.geer@wsu.edu')
        u.set_password('test')
        self.assertFalse(u.get_password('password'))
        self.assertTrue(u.get_password('test'))

    def test_password_hashing_admin(self):
        u = Admin(username='ben', email='ben.geer@wsu.edu')
        u.set_password('test')
        self.assertFalse(u.get_password('password'))
        self.assertTrue(u.get_password('test'))

    def test_review_1(self):
        u1 = User(username='john', email='john.yates@wsu.com')
        db.session.add(u1)
        db.session.commit()

        b1 = Book(title="Title", author="Author")
        self.assertEqual(b1.get_reviews().all, [])
        self.assertEqual(b1.get_reviews().all, [])

        r1 = Review(title="Review Title", body="Review body.")
        b1.reviews.append(r1)
        self.assertEqual(b1.get_reviews().all, [r1])
        self.assertEqual(b1.get_reviews().count(), 1)
        self.assertEqual(b1.get_reviews().first().title, "Review Title")
        self.assertEqual(b1.get_reviews().first().body, "Review body.")


if __name__ == '__main__':
    unittest.main(verbosity=2)