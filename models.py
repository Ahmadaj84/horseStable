from flask_sqlalchemy import SQLAlchemy

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

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    horse_id = db.Column(db.Integer, db.ForeignKey('horses.id'))
    rider_id = db.Column(db.Integer, db.ForeignKey('riders.id'))
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'))

class Coach(db.Model):
    __tablename__ = 'coach'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    