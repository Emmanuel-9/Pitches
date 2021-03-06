from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Pitch(db.Model):
  
    __tablename__ = 'pitches'
    id = db.Column(db.Integer,primary_key = True)
    pitch = db.Column(db.String(255))
    category = db.Column(db.String(255))
    title = db.Column(db.String(255))
    vote_count = db.Column(db.Integer)
    added_date = db.Column(db.DateTime,default = datetime.utcnow)
    author = db.Column(db.Integer,db.ForeignKey('users.id'))

    def __repr__(self):
        return f'Pitch{self.pitch}'


class User(UserMixin,db.Model):
  
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username =  db.Column(db.String(255),index = True)
    email =  db.Column(db.String(255),unique = True,index=True)
    bio = db.Column(db.String(255))
    profile_pic_path  = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    pitches =  db.relationship('Pitch',backref = 'user',lazy='dynamic')
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        self.password_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_secure,password)

    def __repr__(self):
        return f'User {self.username}'

class Comment(db.Model):
 
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    comment = db.Column(db.String(255))
    title = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    poster = db.Column(db.Integer,db.ForeignKey('users.id'))
  
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.comment}'