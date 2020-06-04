
#%%

import requests

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/GetLatLonFromAnAddress?code=ucwQTFn4ivV/uycR72H3o7EIoSC28cDHynS8jFmlZ8Zwuy2iuL4yaQ=='

json_payload = {'address': '15127 NE 24th Street, Redmond, WA'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text




# %%
