from datetime import datetime
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


reviewBook = db.Table('reviewBook',
                   db.Column('review_id', db.Integer, db.ForeignKey('review.id')),
                   db.Column('book_id', db.Integer, db.ForeignKey('book.id')))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    likes = db.Column(db.Integer, default = 0)
    book = db.relationship('Book', 
                            secondary = reviewBook,
                            primaryjoin = (reviewBook.c.review_id == id),
                            backref = db.backref('reviewBook', lazy = 'dynamic'),
                            lazy = 'dynamic')

class Book(db.Model):     ##### not sure if the relationship is how this works? #####
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(30))
    # reviews = db.relationship('Review', back_populates="book")
    
    def __repr__(self):
        return '<id: {} - title: {}, author: {}>'.format(self.id,self.title, self.author)

    def getTitle(self):
        return self.title

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