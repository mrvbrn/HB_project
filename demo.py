# This example uses Python Requests library http://docs.python-requests.org/en/master/
import requests
import json
import os
from flask import jsonify
# Request Parameters


"""API_KEY and password"""

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

store = "android"
country_code = "US"
date = "2019-03-04" # Unique app identifier (bundle ID).

req_params = {"date" : date,
                  "country" : country_code}

request_url = request_url = f"https://api.appmonsta.com/v1/stores/{store}/rankings.json" 
headers = {'Accept-Encoding': 'deflate, gzip'}

    # Python Main Code Sample
response = requests.get(request_url,
                            auth=(username, password),
                            params=req_params,
                            headers=headers,
                            stream=True)

games = []
games_seen = set()
for line in response.iter_lines():
    """Load json object and print it out"""

    game_dict = json.loads(line)
    if game_dict['app_id'] not in games_seen:
        games.append(game_dict)
        games_seen.add(game_dict['app_id'])

game = sorted(games, key=lambda i: i['rank'])[:20]
print(game)

