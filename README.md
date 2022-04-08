# FocusFitness
Here is a link to our web-app [FocusFitness](https://tranquil-spire-20189.herokuapp.com/)

## Lets Work out!
In our web-app we are redefining the way you track and log your workouts! First off is to create an account (using their email and password) to login to our page. Then it'll take you straight to the homepage where you can input what workout you'll be doing, for how long did you do that workout, and also your weight which will all be logged into our database system. Our fantastic calorie calculator will then display an estimate on how much calories you lost during that workout. Within the homepage there is also a calendar function that'll track the days you've logged on, a recent workouts section that'll show the 4 most recent workouts you have input into our system and finally a motivational quote section that'll keep you going to strive for more greatness!

## The Tech We Used
To get this web-app off the ground we used Python/Flask for the backend alongside with SQLAlchemy to hold our user data in our databases. For the front-end we used HTML/CSS along side with bootstrap to help the designing of the web-app easier. Then we launched the app with Heroku so it can be accessible to anybody.

## Some Challenges We Ran Into
This wasn't an easy project to get off the ground at all, and like every other group we ran into some minor bumps along the road. First getting all of our seperate parts together to merge was kind of a hassle, this is our first time working together so we had to make sure that everything seperate part that we did wouldn't break everything when merging. We used a good amount of pull-requests and took our time with these things to finally achieve a successful merge. 

## Setup Instructions
1. `pip3 install -r requirements.txt`
2. Create a `.env` file in the top-level directory and enter the following as its contents:
```
export SECRET_KEY="<YOUR SECRET KEY>"
export DATABASE_URL="<YOUR POSTGRESQL DB URL>"
```
## To run the app
1. Run `python3 app.py`