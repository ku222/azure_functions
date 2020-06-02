
#%%

import requests

DEPLOYED_URL = 'http://cloudwars2functionapp.azurewebsites.net/api/ValidatePhoneNumber?code=WP9NR0mbX2aG9dwWZwgiF2jiVD/CEXy0SmnIZp2u4xS0NmWX7kSVDA=='

json_payload = {'number': ' 42- 32--53-33//13'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

