"""
Database for reviews
ref:
https://overiq.com/flask-101/authentication-in-flask/
"""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import UserMixin

ma = Marshmallow()
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

class RecordSchema(ma.Schema):
    """ Create schema for record table """

    class Meta:
        """ Set model to record """

        fields = ("id", "username", "duration", "weight",
        "exercise_type", "calories_burned")


class User(UserMixin, db.Model):
    """Contains table of our users"""

    # pylint: disable=no-member
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
