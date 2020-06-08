
#%%

import requests

DEPLOYED_URL = 'http://cloudwars2functionapp.azurewebsites.net/api/NavigationBranchFormatter?code=GMtryo1P7lJD3Jq4K7ILowWbTC/HKfM97dZ6bNLqdV3e9xgISHCftw=='

json_payload = {'address': 'Beverly Hills, 90210'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)


#%%

response.text


#%%
