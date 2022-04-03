"""
Wikilink creator
"""
import json
import requests


def get_quote():
    """Returns random quote"""
    base_url = "https://zenquotes.io/api/random"
    # print(base_url)
    params = {}
    response = requests.get(base_url, params=params)
    data = response.json()
    print(json.dumps(response.json(), indent=4, sort_keys=True))
    quote = data[0]["q"]
    print(quote)
    return quote
