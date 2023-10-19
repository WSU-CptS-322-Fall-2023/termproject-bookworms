from datetime import datetime
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    likes = db.Column(db.Integer, default = 0)
    book = db.relationship('BookReview', back_populates="_review")

class Book(db.Model):     ##### not sure if the relationship is how this works? #####
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(30))
    reviews = db.relationship('BookReview', back_populates="_book")
    
    def __repr__(self):
        return '<id: {} - title: {}, author: {}>'.format(self.id, self.title, self.author)

    def getTitle(self):
        return self.title


class BookReview(db.Model):
    bookTitle = db.Column(db.String(150), db.ForeignKey('book.title'), primary_key = True)
    reviewId = db.Column(db.Integer,db.ForeignKey('review.id'), primary_key = True)
    primary = db.Column(db.Boolean)
    _review = db.relationship('Review')
    _book = db.relationship('Book')
    def __repr__(self):
        return '<BookReview ({}, {}, {})>'.format(self.bookTitle, self.reviewId, self.primary)


class User(UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {} - {} {} - {};>'.format(self.id, self.username, self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password_hash, password)