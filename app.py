"""
FocusFitness
"""
import os
import random
import flask
from flask import Flask, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    current_user,
    logout_user,
)

from quotes import get_quote
from database import db, Users

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

"""LOGIN INFO"""
app.secret_key = os.getenv("SECRET_KEY")

"""DATABASE SETUP"""
# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
        "SQLALCHEMY_DATABASE_URI"
    ].replace("postgres://", "postgresql://")


db.init_app(app)

# used to prevent circular imports
with app.app_context():
    db.create_all()

### Flask Login
login_manager = LoginManager()
login_manager.login_view = "index"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(login_name):
    """query for user"""
    return Users.query.get(login_name)


@app.route("/")
def index():
    """Returns login screen"""
    return flask.render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """signup and save username to database"""
    if flask.request.method == "POST":
        data = flask.request.form
        username = data["username"]
        password = data["password"]
        user = Users.query.filter_by(login_name=username).first()
        print(user)
        if user:
            flask.flash("User already exsits")
            return flask.redirect(flask.url_for("signup"))

        new_user = Users(
            login_name=data["username"],
            password_hash=generate_password_hash(password, method="sha256"),
        )
        # pylint: disable=no-member
        db.session.add(new_user)
        db.session.commit()
        print("user created")
        print(data["username"])
        return flask.redirect(flask.url_for("index"))
    return render_template(
        "signup.html",
    )


@app.route("/handle_form", methods=["POST"])
def handle_form():
    """returns login form checking and redirect"""

    data = flask.request.form
    username = data["username"]
    password = data["password"]
    user = Users.query.filter_by(login_name=username).first()
    print(user)
    if not user or not check_password_hash(user.password_hash, password):
        flask.flash("Please check your login details and try again.")
        return flask.redirect(
            flask.url_for("index")
        )  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return flask.redirect(flask.url_for("discovery"))


@app.route("/discovery")
@login_required
def discovery():

    # only display comments when one exists for the movie

    return render_template(
        "discovery.html",
        name=current_user.login_name,
        quote=get_quote(),
    )


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """logout function"""
    logout_user()
    return flask.redirect(flask.url_for("index"))


@app.errorhandler(404)
# pylint: disable=unused-argument
def page_not_found(error):
    """error handling; redirect to 404.html"""
    return render_template("404.html"), 404


app.run(
    host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
)
