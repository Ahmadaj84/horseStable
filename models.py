from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from datetime import datetime

db = SQLAlchemy()

class Horse(db.Model):
    __tablename__ = 'horses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)

class Rider(db.Model):
    __tablename__ = 'riders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    level = db.Column(db.String(50))
    email = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('class_user' , lazy=True) )

class Trining_class(db.Model):
    __tablename__ = 'training_class'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    horse_id = db.Column(db.Integer, db.ForeignKey('horses.id'))
    rider_id = db.Column(db.Integer, db.ForeignKey('riders.id'))
    paddock_id = db.Column(db.Integer, db.ForeignKey('paddock.id'))

    horse = db.relationship('Horse', backref=db.backref('class_horse', lazy=True))
    rider = db.relationship('Rider', backref=db.backref('class_rider', lazy=True))
    paddock = db.relationship('Paddock', backref=db.backref('padadock_class', lazy=True))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    mobile = db.Column(db.String(150), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(30), nullable=False)

@event.listens_for(User, "after_insert")
def create_ryder(mapper, connection, target):
    session = db.session.object_session(target)
    rider = Rider(user_id=target.id,name=target.fullname , level="مبتدئ" , email=target.email,mobile=target.mobile)
    session.add(rider)

class RiderSub(db.Model):
    __tablename__ = 'rider_sub'

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    rider_id = db.Column(db.Integer, db.ForeignKey('riders.id'), nullable=False)
    active = db.Column(db.Boolean, default=True)

    rider = db.relationship('Rider', backref=db.backref('subscriptions', lazy=True))

class Paddock(db.Model):
     __tablename__ = 'paddock'
     id = db.Column(db.Integer, primary_key=True)
     paddock_name = db.Column(db.String(100), unique=True, nullable=False)
     capacity = db.Column(db.Integer, nullable = False)
        
