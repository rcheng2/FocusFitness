"""
Quotes Generator
"""
import json
import requests


def get_quote():
    """Returns random quote"""
    base_url = "https://zenquotes.io/api/random"
    params = {}
    response = requests.get(base_url, params=params)
    data = response.json()
    quote = data[0]["q"]
    return quote
