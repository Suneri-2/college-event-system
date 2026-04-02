from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------------------------
# User Table
# ---------------------------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    

# ---------------------------
# Event Table
# ---------------------------
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)


# ---------------------------
# Registration Table
# ---------------------------
class Registration(db.Model):
    __tablename__ = 'registrations'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    semester = db.Column(db.String(50))   # FIXED NAME
    roll_no = db.Column(db.String(50))

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ---------------------------
# Notification Table
# ---------------------------
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)   # ADDED
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(20), default=datetime.utcnow().strftime("%Y-%m-%d"))

# ---------------------------
# Announcement Table
# ---------------------------
class Announcement(db.Model):
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text)   # FIXED (was description)
    date = db.Column(db.String(20), default=datetime.utcnow().strftime("%Y-%m-%d"))