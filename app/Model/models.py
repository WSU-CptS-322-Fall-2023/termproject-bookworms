from datetime import datetime
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

reviewBook = db.Table('reviewBook', db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                    db.Column('review_id', db.Integer, db.ForeignKey('review.id')))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    likes = db.Column(db.Integer, default = 0)
    # book = db.Column(db.Integer, db.ForeignKey('book.id'))

    #book = db.relationship('BookReview', back_populates="_review"


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
    

class Book(db.Model):     ##### not sure if the relationship is how this works? #####
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(30))
    year = db.Column(db.Integer, db.ForeignKey('year.year'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    reviews = db.relationship('Review', secondary = reviewBook, primaryjoin=(reviewBook.c.book_id == id), 
                           backref=db.backref('reviewBook', lazy='dynamic'), lazy='dynamic' )
    def __repr__(self):
        return '<id: {} - title: {}, author: {}>'.format(self.id, self.title, self.author)

    def getTitle(self):
        return self.title

    # reviews = db.relationship('Review', back_populates="book")

class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    books = db.relationship('Book', backref='bookyear', lazy='dynamic')

