
#%%

import requests

DEPLOYED_URL = 'http://cloudwars2functionapp.azurewebsites.net/api/ValidateAddress?code=BA77aXBrSHU0L7hb4FQkvxfoK/VHVYfAEdbEwqCNoBcbwYOWRzQOog=='
json_payload = {'address': '15127 NE 24th Street, Redmond, WA'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)



# %%
response.json()