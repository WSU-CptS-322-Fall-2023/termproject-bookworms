from datetime import datetime
from app import db, login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

reviewBook = db.Table('reviewBook', db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                    db.Column('review_id', db.Integer, db.ForeignKey('review.id')))

reviewUser = db.Table('reviewUser', db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('review_id', db.Integer, db.ForeignKey('review.id')))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    likes = db.Column(db.Integer, default = 0)
    # book = db.Column(db.Integer, db.ForeignKey('book.id'))

    #book = db.relationship('BookReview', back_populates="_review"


class User(UserMixin, db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(50))
    reviews = db.relationship('Review', secondary = reviewUser, primaryjoin=(reviewUser.c.user_id == id), 
                           backref=db.backref('reviewUser', lazy='dynamic'), lazy='dynamic' )

    __mapper_args__ = {
        'polymorphic_identity': 'User',
        'polymorphic_on': user_type
    }

    def __repr__(self):
        return '<User {} - {} - {};>'.format(self.id, self.username, self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Admin(User):
    __tablename__='admin'
    id = db.Column(db.ForeignKey("user.id"), primary_key = True)

    __mapper_args__ = {
        'polymorphic_identity': 'Admin'
    }

class Regular_User(User):
    __tablename__='reg_user'
    id = db.Column(db.ForeignKey("user.id"), primary_key = True)

    __mapper_args__ = {
        'polymorphic_identity': 'Reg_User'
    }
    

class Book(db.Model):     ##### not sure if the relationship is how this works? #####
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(30))
    year = db.Column(db.Integer, db.ForeignKey('year.year'))
    genres = db.relationship('Roster', back_populates="bookgenres")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    reviews = db.relationship('Review', secondary = reviewBook, primaryjoin=(reviewBook.c.book_id == id), 
                           backref=db.backref('reviewBook', lazy='dynamic'), lazy='dynamic' )
    def __repr__(self):
        return '<id: {} - title: {}, author: {}>'.format(self.id, self.title, self.author)

    def getTitle(self):
        return self.title
    
    def getGenres(self):
        return self.genres
    
    def addGenre(self, newGenre):
        newG = Roster(genres = newGenre)
        self.genres.append(newG)
        db.session.commit()

    # reviews = db.relationship('Review', back_populates="book")

class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    books = db.relationship('Book', backref='bookyear', lazy='dynamic')

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    roster = db.relationship('Roster', back_populates="genres")

    def __repr__(self):
        return '{}'.format(self.name)


class Roster(db.Model):
    bookid = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    genreid = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)
    bookgenres = db.relationship('Book')
    genres = db.relationship('Genre')
