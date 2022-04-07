import os
import hashlib
import flask
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template
from flask_login import login_required
from quotes import get_quote
from flask_sqlalchemy import SQLAlchemy
from database import Record, User, db


# imports for login
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)


load_dotenv(find_dotenv())


# from database import db, Users, Record

app = Flask(__name__)
app.secret_key = os.getenv("app.secret_key")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initializing login manager
login_manager = LoginManager()
login_manager.init_app(app)


# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(16))


# db.create_all()


# """DATABASE SETUP"""
# # Point SQLAlchemy to your Heroku database
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# # Gets rid of a warning
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
        "SQLALCHEMY_DATABASE_URI"
    ].replace("postgres://", "postgresql://") """


db.init_app(app)

# used to prevent circular imports
# with app.app_context():
#     db.create_all()

# All of this is for login and authentication stuff
def hashedpass(ptext):
    plaintext = ptext.encode()
    d = hashlib.sha3_256(plaintext)
    hash = d.hexdigest()
    return hash


@app.route("/")
def login():
    return flask.render_template("login.html")


@app.route("/signuppage", methods=["POST"])
def signuppage():
    return flask.redirect(flask.url_for("signup"))


@app.route("/signuppage")
def signup():
    return flask.render_template("signup.html")


@app.route("/main")
@login_required
def main():
    currentuser = current_user.username
    return flask.render_template("index.html", currentuser=currentuser)


@app.route("/registernewuser", methods=["POST"])
def registernewuser():
    try:
        data = flask.request.form
        user_id = data["newuserid"]
        password = data["newpassword"]
        hashed = hashedpass(password)
        new_user = User(username=user_id, password=hashed)
        db.session.add(new_user)
        db.session.commit()
        flask.flash("User Successfully Created. Try logging in!")
        return flask.redirect(flask.url_for("login"))
    except:
        flask.flash("This user already exists, Usernames must be unique. Try again")
        return flask.redirect(flask.url_for("signup"))


# Method of logging in users
# Takes the user to the main page if login is successful otherwise it returns them to the same login page
@app.route("/loginuser", methods=["POST"])
def loginuser():
    data = flask.request.form
    user_id = data["userid"]
    pwd = data["pwd"]
    hashed = hashedpass(pwd)

    user = User.query.filter_by(username=user_id, password=hashed).first()

    try:
        if login_user(user):
            return flask.redirect(flask.url_for("index"))

    except:
        flask.flash(
            "User does not exist or you entered the wrong credentials. Try Again!"
        )
        return flask.redirect(flask.url_for("login"))


@app.route("/logoff", methods=["POST"])
def logout():
    logout_user()
    flask.flash("You have been logged out!")
    return flask.redirect(flask.url_for("login"))


# Required part of Flask-Login for loading users
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Until Here


@app.route("/index")
@login_required
def index():
    """Returns login screen"""
    quote = get_quote()
    currentuser = current_user.username
    return flask.render_template(
        "home.html", quote=get_quote(), currentuser=currentuser
    )


# @app.route("/home")
# def home():
#     """Returns quote from api"""
#     quote = get_quote()
#     return render_template(
#         "home.html",
#         quote=get_quote(),
#     )


@app.errorhandler(404)
# pylint: disable=unused-argument
def page_not_found(error):
    """error handling; redirect to 404.html"""
    return render_template("404.html"), 404


@app.route("/workouts")
def workouts():
    """Returns login screen"""
    quote = get_quote()
    return flask.render_template(
        "workouts.html",
    )


@app.route("/calculate", methods=["POST"])
def calculate():
    """Route to calculate calories burned and write to database"""
    if flask.request.method == "POST":
        duration = int(flask.request.values.get("duration"))
        weight = int(flask.request.values.get("weight"))
        exercise_type = flask.request.values.get("exercise_type")

        if exercise_type == "cardio":
            met = 7
        elif exercise_type == "weightlifting":
            met = 5
        else:
            met = 3

        calories_burned = duration * (met * 3.5 * weight) / 200

        new_record = Record(
            username="username",
            duration=duration,
            weight=weight,
            exercise_type=exercise_type,
            calories_burned=calories_burned,
        )

        db.session.add(new_record)
        db.session.commit()

        return flask.render_template(
            "home.html", calories_burned=calories_burned, quote=get_quote()
        )

    return flask.render_template("home.html", quote=get_quote())


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
    )
