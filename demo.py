# This example uses Python Requests library http://docs.python-requests.org/en/master/
import requests
import json
import os
# Request Parameters
store = "android"       # Could be either "android" or "itunes".
country_code = "US"     # Two letter country code.
date = "2019-02-17"     # Date in YYYY-MM-DD format.

req_params = {"date": date,
              "country": country_code}

# Auth Parameters
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')          # Password can be anything.

# Request URL
request_url = "https://api.appmonsta.com/v1/stores/%s/rankings.json" % store

# This header turns on compression to reduce the bandwidth usage and transfer time.
headers = {'Accept-Encoding': 'deflate, gzip'}

# Python Main Code Sample
response = requests.get(request_url,
                        auth=(username, password),
                        params=req_params,
                        headers=headers,
                        stream=True)

print (response.status_code)
for line in response.iter_lines():
  # Load json object and print it out
  json_record = json.loads(line)
  print (json_record)