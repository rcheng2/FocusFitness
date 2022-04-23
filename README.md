# FocusFitness
Here is a link to our app [FocusFitness](https://floating-ravine-92058.herokuapp.com/)

## Lets Work out!
In our web-app we are redefining the way you track and log your workouts! First off you will be greeted by our beautiful landing page where you can read up about features specific to this app and the names of the developers that worked to bring this project together. You'll also see there are 2 large buttons where you could either **Login** or **Signup** (using your email and password) to then land on our homepage. **This** is where the magic happens when you get to see all of our wonderful features in the app consisting of a working **Calorie Calculator** that will allow you to input any workout on the dropdown list and the date (along with how long you were working out and your weight) and it'll calculate how many estimated calories you've burned for that workout! Amazing right? Along side the Calore Calculator is a functioning **Calendar** that actively updates anytime you input a workout so you could keep track of all the workouts that has been done and put on our app. Last but not least we have a **Motivational Quote Generator** that would give you a new quote any time you press the button below or refresh the page. On our navigation bar we have 4 options: Home, History, Workouts, and Log out. 

Once you click the **History** tab you'll be taken to a page where you could see all of the workouts you've put into our database along with a couple of new features, our Edit and Delete button will allow you to have absolute free functionality to change the Date, Weight, Duration, and Exercise Type. 

Next we have the **Workouts** tab which will take you to a different page that will display youtube videos that will show you how to do a certain workout. It has a drop down menu with more then 8 workouts that will help you get that perfect form! 

Lastly the **Logout** button well.. logs you out of our app and will take you back to the landing page. Thank you for exploring FocusFitness!

## The Tech We Used
To get this web-app off the ground we used Python/Flask for the backend alongside with SQLAlchemy to hold our user data in our databases. For the front-end we used HTML/CSS/JavaScript along side with bootstrap to help the designing of the web-app easier. Then we launched the app with Heroku so it can be accessible to anybody.

## Some Challenges We Ran Into
This wasn't an easy project to get off the ground at all, and like every other group we ran into some minor bumps along the road. First getting all of our seperate parts together to merge was kind of a hassle, this is our first time working together so we had to make sure that everything seperate part that we did wouldn't break everything when merging. We used a good amount of pull-requests and took our time with these things to finally achieve a successful merge. 

## Unit Test Issues
We changed all the tests from local to github action tests. We chose to test database using a sqlite database and testing it in memory. Since we only used one API for the quote and did sqlite for database testing, we only have one mock test.

## Setup Instructions
1. `pip3 install -r requirements.txt`
2. Create a `.env` file in the top-level directory and enter the following as its contents:
```
export SECRET_KEY="<YOUR SECRET KEY>"
export DATABASE_URL="<YOUR POSTGRESQL DB URL>"
```
## To run the app
1. Run `python3 app.py`


## Heroku Sprint 1
Here is a link to our Sprint 1 [FocusFitness](https://tranquil-spire-20189.herokuapp.com/) 
