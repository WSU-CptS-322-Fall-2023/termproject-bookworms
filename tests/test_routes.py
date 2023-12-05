
import sys
sys.path.insert(0, 'D:\DOCS\Fall 2023\CPTS 322\Term Project') # my directory

import os
import unittest
from app import create_app, db
from app.Model.models import Book, Genre, Year, User
from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    DEBUG = True
    TESTING = True



class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_post_review_route_authenticated(self):
        with self.app.test_request_context('/postreview<book_id>', method='POST'):
            # Simulate an authenticated user
            with self.app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['user_id'] = 1

                response = client.post('/postreview1', data={'title': 'Test Title', 'body': 'Test Body'})
                self.assertEqual(response.status_code, 302)

    def test_add_book_route_authenticated_as_admin(self):
        with self.app.test_request_context('/addbook', method='POST'):
            with self.app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['user_id'] = 1 

                response = client.post('/addbook', data={'title': 'Test Title', 'author': 'Test Author'})
                self.assertEqual(response.status_code, 302) 


    def test_suggest_book_route_authenticated_as_user(self):
        with self.app.test_request_context('/suggestbook', method='POST'):
            with self.app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['user_id'] = 1

                response = client.post('/suggestbook', data={'title': 'Test Title', 'author': 'Test Author'})
                self.assertEqual(response.status_code, 200)  

if __name__ == '__main__':
    unittest.main()
