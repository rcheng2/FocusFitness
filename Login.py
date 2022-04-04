import flask
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)

app = flask.Flask(__name__)
app.secret_key = os.getenv("app.secret_key")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(16))


db.create_all()


@app.route("/")
def login():
    return flask.render_template("login.html")


@app.route("/signuppage", methods=["POST"])
def signuppage():
    return flask.redirect(flask.url_for("signup"))


@app.route("/signuppage")
def signup():
    return flask.render_template("signup.html")


@login_required
@app.route("/main")
def main():
    currentuser = current_user.username
    return flask.render_template("index.html", currentuser=currentuser)


@app.route("/registernewuser", methods=["POST"])
def registernewuser():
    try:
        data = flask.request.form
        user_id = data["newuserid"]
        password = data["newpassword"]
        new_user = User(username=user_id, password=password)
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

    user = User.query.filter_by(username=user_id, password=pwd).first()

    try:
        if login_user(user):
            return flask.redirect(flask.url_for("main"))

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


app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)

