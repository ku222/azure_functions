
#%%

import requests
import json

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/ValidatePINInput?code=Ha2O093ALfx4ba0mKmadDGYvZueSJpQyBvEv5z9UKsd7xffENNyYrw=='
json_payload = {'PIN': '4447'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

