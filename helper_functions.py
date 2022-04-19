"""
Quotes Generator
"""
import requests


def get_quote():
    """Returns random quote"""
    base_url = "https://zenquotes.io/api/random"
    params = {}
    response = requests.get(base_url, params=params)
    data = response.json()
    quote = data[0]["q"]
    return quote

def get_calories_burned(duration, weight, exercise_type):
    """ function to calculate calories burned"""
    super_vigorous_exercise = ["Running", "Swimming",
    "Crossfit", "Rowing", "Mountain Biking",
    "Rock Climbing", "Gymnastics", "Rugby", "Football",
    "Soccer", "Water Polo", "Wrestling", "Martial arts",
    "Calisthenics"]
    vigorous_exercise = ["Beach Volleyball",
    "Cycling", "Lacrosse", "Skateboarding", "Ultimate Frisbee",
    "Weightlifting"]
    moderate_exercise = ["Jogging", "Jump Rope", "Baseball",
    "Yoga", "Dancing"]
    if exercise_type in super_vigorous_exercise:
        met = 7
    elif exercise_type in vigorous_exercise:
        met = 6
    elif exercise_type in moderate_exercise:
        met = 5
    else:
        met = 3

    calories_burned = duration * (met * 3.5 * weight) / 200

    return calories_burned