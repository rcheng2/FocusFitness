# pylint: disable = import-error, invalid-envvar-default, unused-import
""" File to run heroku app """
import os
from dotenv import find_dotenv, load_dotenv
import flask # type: ignore
from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Record(db.Model):
    """ Table for exercise records """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    duration = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    exercise_type = db.Column(db.String())
    calories_burned = db.Column(db.String())

@app.route("/")
def index():
    """ function to render index.html """
    return flask.render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    """ Route to calculate calories burned and write to database """
    if flask.request.method == 'POST':
        duration = int(flask.request.values.get("duration"))
        weight = int(flask.request.values.get("weight"))
        exercise_type = flask.request.values.get("exercise_type")

        if exercise_type == "cardio":
            met = 7
        elif exercise_type == "weightlifting":
            met = 5
        else:
            met = 3

        calories_burned = duration * ( met * 3.5 * weight) / 200

        new_record = Record(username="username",
        duration=duration,
        weight=weight,
        exercise_type=exercise_type,
        calories_burned=calories_burned)

        db.session.add(new_record)
        db.session.commit()

        return flask.render_template("index.html", calories_burned=calories_burned)

    return flask.render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
