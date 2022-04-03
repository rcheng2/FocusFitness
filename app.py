"""
FocusFitness
"""
import os

import flask
from flask import Flask, render_template
from dotenv import find_dotenv, load_dotenv
from quotes import get_quote

load_dotenv(find_dotenv())
from database import db, Users, Record

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# """DATABASE SETUP"""
# # Point SQLAlchemy to your Heroku database

# # Gets rid of a warning


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)
db.init_app(app)
if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
        "SQLALCHEMY_DATABASE_URI"
    ].replace("postgres://", "postgresql://")


# # used to prevent circular imports
# with app.app_context():
#     db.create_all()


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

        return flask.render_template("index.html", calories_burned=calories_burned)

    return flask.render_template("index.html")


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


app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)
