
#%%

import requests

DEPLOYED_URL = 'http://cloudwars2functionapp.azurewebsites.net/api/ValidatePINStrength?code=SsjG8i3VjwFGEJyZKuEh5g/rHzu3thZWO4bFUiPTB19HM0iNIGFogQ=='
json_payload = {'NI': '4490'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text


#%%

