# This example uses Python Requests library http://docs.python-requests.org/en/master/
import requests
import json
import os
from flask import jsonify
# Request Parameters


# Request Parameters
store = "android"       # Could be either "android" or "itunes".
country_code = "US"     # Two letter country code.
app_id = "com.androbaby.game2048" # Unique app identifier (bundle ID).

req_params = {"country": country_code}

# Auth Parameters
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')       # Password can be anything.

url = "https://api.appmonsta.com/v1/stores/%s/details/%s.json" % (store, app_id)

# This header turns on compression to reduce the bandwidth usage and transfer time.
headers = {'Accept-Encoding': 'deflate, gzip'}

# Python Main Code Sample
response = requests.get(url,
                        auth=(username, password),
                        params=req_params,
                        headers=headers,
                        stream=True)

print (response.status_code)
for line in response.iter_lines():# Load json object and print it out
  json_record = json.loads(line)
  games = json_record['all_histogram']
  rating = json_record['all_rating']
  print(json_record['all_histogram'])
  print(rating)


