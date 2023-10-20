from datetime import datetime
from app import db, login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    likes = db.Column(db.Integer, default = 0)

class User(UserMixin, db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(50))

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

