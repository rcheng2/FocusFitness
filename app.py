"""All the main imports we need"""
import os
import hashlib
import flask
from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template, request


# imports for login
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from helper_functions import get_calories_burned, get_quote
from database import Record, User, db


load_dotenv(find_dotenv())

app = Flask(__name__)  # pylint: disable= invalid-name
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initializing login manager
login_manager = LoginManager()  # pylint: disable= invalid-name
login_manager.init_app(app)


if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config[
        "SQLALCHEMY_DATABASE_URI"
    ].replace("postgres://", "postgresql://")


db.init_app(app)

# used to prevent circular imports
with app.app_context():
    db.create_all()

# All of this is for login and authentication stuff
def hashedpass(ptext):
    """Returns a hashed password when this function is called"""
    plaintext = ptext.encode()
    _d = hashlib.sha3_256(plaintext)
    phash = _d.hexdigest()
    return phash


@app.route("/")
def login():
    """The first screen the user sees"""
    return flask.render_template("landing.html")


@app.route("/login")
def land():
    """LOGIN PAGE"""
    return render_template("login.html")


@app.route("/signuppage", methods=["POST"])
def signuppage():
    """Redirects the user a sign up screen"""
    return flask.redirect(flask.url_for("signup"))


@app.route("/signuppage")
def signup():
    """Returns the user a sign up screen"""
    return flask.render_template("signup.html")


@app.route("/registernewuser", methods=["POST"])
def registernewuser():
    """Function to register a new user to the db"""
    try:
        data = flask.request.form
        user_id = data["newuserid"]
        password = data["newpassword"]
        hashed = hashedpass(password)
        new_user = User(username=user_id, password=hashed)
        # pylint: disable=no-member
        db.session.add(new_user)
        db.session.commit()
        flask.flash("User Successfully Created. Try logging in!")
        return flask.redirect(flask.url_for("land"))
    except:  # pylint: disable=bare-except
        flask.flash("This user already exists, Usernames must be unique. Try again")
        return flask.redirect(flask.url_for("signup"))


# Method of logging in users
# Takes the user to the main page if login is
# successful otherwise it returns them to the same login page
@app.route("/loginuser", methods=["POST"])
def loginuser():
    """Flask function to login user"""
    data = flask.request.form
    user_id = data["userid"]
    pwd = data["pwd"]
    hashed = hashedpass(pwd)

    user = User.query.filter_by(username=user_id, password=hashed).first()

    try:
        if login_user(user):
            return flask.redirect(flask.url_for("index"))
        return flask.redirect(flask.url_for("login"))

    except:  # pylint: disable=bare-except
        flask.flash(
            "User does not exist or you entered the wrong credentials. Try Again!"
        )
        return flask.redirect(flask.url_for("land"))


@app.route("/logoff", methods=["POST"])
def logout():
    """Flask login function for logging a user out"""
    logout_user()
    flask.flash("You have been logged out!")
    return flask.redirect(flask.url_for("login"))


# Required part of Flask-Login for loading users
@login_manager.user_loader
def load_user(user_id):
    """Flask login function for logging a user out"""

    return User.query.get(int(user_id))


# Until Here


@app.route("/index")
@login_required
def index():
    """Returns main app page after logging in"""
    quote = get_quote()
    currentuser = current_user.username
    events = Record.query.filter_by(username=current_user.username).all()
    return flask.render_template(
        "home.html", quote=quote, currentuser=currentuser, events=events
    )


@app.errorhandler(404)
# pylint: disable=unused-argument
def page_not_found(error):
    """error handling; redirect to 404.html"""
    return render_template("404.html"), 404


@app.route("/workouts")
def workouts():
    """Returns login screen"""
    return flask.render_template(
        "workouts.html",
    )



@app.route("/calculate", methods=["POST", "GET"])
def calculate():
    """Route to calculate calories burned and save workout to database"""
    currentuser = current_user.username
    quote = get_quote()
    if flask.request.method == "POST":
        duration = int(flask.request.values.get("duration"))
        weight = int(flask.request.values.get("weight"))
        exercise_type = flask.request.values.get("exercise_type")
        timestamp = flask.request.values.get("date")
        print(timestamp)
        calories_burned = get_calories_burned(duration, weight, exercise_type)
        display_calories_burned = f"You burned {calories_burned} calories!!!"

        new_record = Record(
            username=currentuser,
            duration=duration,
            weight=weight,
            timestamp=timestamp,
            exercise_type=exercise_type,
            calories_burned=calories_burned,
        )

        # pylint: disable=no-member
        db.session.add(new_record)
        db.session.commit()


        events = Record.query.filter_by(username=current_user.username).all()
        num_events = len(events)
        return flask.render_template(
            "home.html",
            display_calories_burned=display_calories_burned,
            quote=quote,
            currentuser=currentuser,
            events=events,
            num_events=num_events,
        )

    return flask.render_template("home.html", quote=quote, currentuser=currentuser)


@app.route("/history", methods=["POST", "GET"])
@login_required
def load_history():
    """Route to load previous workouts"""

    username = current_user.username
    prev_workouts = (
        Record.query.filter_by(username=username).order_by(Record.timestamp.asc()).all()
    )
    num_workouts = len(prev_workouts)

    return flask.render_template(
        "history.html", prev_workouts=prev_workouts, num_workouts=num_workouts
    )


@app.route("/getinput", methods=["GET"])
@login_required
def getinput():
    """Loads the workouts page for the user make a selection"""
    return flask.render_template(
        "vworkouts.html", video="https://www.youtube.com/embed/vthMCtgVtFw"
    )


@app.route("/vworkouts", methods=["POST"])
@login_required
def vworkouts():
    """Loads the workouts with the user selected workout video"""
    selection = flask.request.form.get("selection")

    my_dict = {
        "Benchpress": "https://www.youtube.com/embed/vthMCtgVtFw",
        "Squats": "https://www.youtube.com/embed/nEQQle9-0NA",
        "Lunges": "https://www.youtube.com/embed/QOVaHwm-Q6U",
        "Deadlifts": "https://www.youtube.com/embed/hCDzSR6bW10",
        "Shoulder Press": "https://www.youtube.com/embed/qEwKCR5JCog",
        "Bicep Curls": "https://www.youtube.com/embed/yTWO2th-RIY",
        "Burpees": "https://www.youtube.com/embed/dZgVxmf6jkA",
        "Pull Ups": "https://www.youtube.com/embed/fO3dKSQayfg",
        "Lat Pulldowns": "https://www.youtube.com/embed/OcFCHdQHjVU",
        "Push Ups": "https://www.youtube.com/embed/IODxDxX7oi4",
        "Hip Thrusts": "https://www.youtube.com/embed/xDmFkJxPzeM",
        "10 Minute Abs Workout": "https://www.youtube.com/embed/zzD80vCLq0Y",
        "Dumbbell Shrugs": "https://www.youtube.com/embed/cJRVVxmytaM",
        "Tricep Extensions": "https://www.youtube.com/embed/PwOwL4B6iw4",
        "Tricep Kickback": "https://www.youtube.com/embed/6SS6K3lAwZ8",
    }
    workout = my_dict.get(selection)

    return flask.render_template(
        "vworkouts.html", video=workout, workoutType=selection, selection=selection
    )



@app.route("/delete/<int:workout_id>", methods=["POST", "GET"])
@login_required
def delete(workout_id):
    """Route to delete a previous workout from database"""

    Record.query.filter_by(id=workout_id).delete()
    db.session.commit()  # pylint: disable=no-member

    username = current_user.username
    prev_workouts = (
        Record.query.filter_by(username=username).order_by(Record.timestamp.asc()).all()
    )
    num_workouts = len(prev_workouts)

    return render_template(
        "history.html", prev_workouts=prev_workouts, num_workouts=num_workouts
    )


@app.route("/modify/<int:workout_id>", methods=["POST", "GET"])
@login_required
def modify(workout_id):
    """Route to load a page to edit selected workout"""
    workout = Record.query.filter_by(id=workout_id).first()

    return render_template("modify.html", workout=workout)


@app.route("/edit", methods=["POST", "GET"])
@login_required
def edit():
    """Route to edit selected previous workout
    and update row in database"""
    workout_id = request.form.get("id")
    timestamp = request.form.get("timestamp")
    exercise_type = request.form.get("exercise_type")
    duration = int(request.form.get("duration"))
    weight = int(request.form.get("weight"))
    calories_burned = get_calories_burned(duration, weight, exercise_type)

    workout = Record.query.filter_by(id=workout_id).first()
    workout.duration = duration
    workout.weight = weight
    workout.exercise_type = exercise_type
    workout.timestamp = timestamp
    workout.calories_burned = calories_burned
    db.session.commit()  # pylint: disable=no-member

    username = current_user.username
    prev_workouts = (
        Record.query.filter_by(username=username).order_by(Record.timestamp.asc()).all()
    )
    num_workouts = len(prev_workouts)

    return render_template(
        "history.html", prev_workouts=prev_workouts, num_workouts=num_workouts
    )


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
    )
