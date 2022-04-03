# pylint: disable = import-error, invalid-envvar-default, unused-import
""" File to run heroku app """

import random
import os
import flask # type: ignore

app = flask.Flask(__name__)


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
        type = flask.request.values.get("type")

        if type is "cardio":
            met = 4
        else:
            met = 2
        
        calories_burned = (duration * met * weight) / 200
        print(calories_burned)
        return flask.render_template("index.html", calories_burned=calories_burned)

    else:
        return flask.render_template("index.html")

app.run(debug=True)
