
#%%

import requests
import json

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/ValidatePINInput?code=Ha2O093ALfx4ba0mKmadDGYvZueSJpQyBvEv5z9UKsd7xffENNyYrw=='
json_payload = {'PIN': '4447'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%%

import re

def validate_and_clean_name(name_str):
    valid = True
    # Search for any non-legal chars
    valid = False if re.search(pattern=r"[^a-zA-Z'\s-]", string=name_str) else valid
    # Search for any consecutive non letters
    valid = False if re.search(pattern=r"[^a-zA-Z]{2}", string=name_str) else valid
    # Now clean up
    if valid:
        splitted = name_str.split(' ')
        titled = [word.title() for word in splitted]
        joined = ' '.join(titled)
        return joined
    return valid

