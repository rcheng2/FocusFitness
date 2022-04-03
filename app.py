"""
FocusFitness
"""
import os

import flask
from flask import Flask, render_template
from quotes import get_quote

# from database import db, Users

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# """DATABASE SETUP"""
# # Point SQLAlchemy to your Heroku database
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# # Gets rid of a warning
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
#     app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
#         "SQLALCHEMY_DATABASE_URI"
#     ].replace("postgres://", "postgresql://")


# db.init_app(app)

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


app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)
