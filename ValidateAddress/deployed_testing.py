
#%%

import requests

DEPLOYED_URL = 'http://cloudwars2functionapp.azurewebsites.net/api/ParseAddress?code=W27MQ3yKWlESaekzA7lRhGMpsX0Tm1egLLH6eE7DNO6/XMk/V7t/5Q=='

json_payload = {'address': '15127 NE 24th Street, Redmond, WA'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text


