
#%%

import requests
import json

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/UpdateProfileFillForm?code=QF9EvYcS0egg5CgLJcHh83saFNgNy38oUQIjVtXrQ3wKOdaaE37yfQ=='
json_payload = {"account_id": 'A00000001'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%% Example payload in dict form
