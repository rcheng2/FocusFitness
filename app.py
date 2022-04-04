import os

import flask
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template
from quotes import get_quote
from flask_sqlalchemy import SQLAlchemy
from database import Record, db

load_dotenv(find_dotenv())

# from database import db, Users, Record

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# """DATABASE SETUP"""
# # Point SQLAlchemy to your Heroku database
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# # Gets rid of a warning
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
        "SQLALCHEMY_DATABASE_URI"
    ].replace("postgres://", "postgresql://")


db.init_app(app)

# # used to prevent circular imports
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    """Returns login screen"""
    quote = get_quote()
    print(quote)
    print("quote")
    return flask.render_template(
        "home.html",
        quote=get_quote(),
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
    print(quote)
    print("quote")
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
