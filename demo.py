# This example uses Python Requests library http://docs.python-requests.org/en/master/
import requests
import json
import os
# Request Parameters
store = "itunes"       # Could be either "android" or "itunes".
country_code = "US"     # Two letter country code.
app_id = "1171299921" # Unique app identifier (bundle ID).

req_params = {"country": country_code}

# Auth Parameters
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')       # Password can be anything.

# Request URL
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
for line in response.iter_lines():
  # Load json object and print it out
  json_record = json.loads(line)
  print (json_record["app_name"])
