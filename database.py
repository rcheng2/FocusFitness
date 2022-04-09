"""
Database for reviews
ref:
https://overiq.com/flask-101/authentication-in-flask/
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

# pylint: disable=too-few-public-methods


class Record(db.Model):
    """Table for exercise records"""

    # pylint: disable=no-member
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    duration = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    exercise_type = db.Column(db.String())
    calories_burned = db.Column(db.String())


class User(UserMixin, db.Model):
    """Contains table of our users"""

    # pylint: disable=no-member
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
