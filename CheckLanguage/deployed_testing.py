
#%%

import requests
import json

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/ViewProfile?code=pa7gOnUTxIPwEeN13gHpeN4gqgkg9agdZZh/XTjC2ABquysNfZDYLQ=='
json_payload = {"account_id": 'A00000001'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%% Example payload in dict form
# u'\u2588'

from adaptivecardbuilder import *
import requests
import json

message = "Cómo estás hoy"

def detect_language(string_list, translator_key="e8662f21ef0646a8abfab4f692e441ab"):
    base_url="https://api.cognitive.microsofttranslator.com/detect?api-version=3.0"
    translator_key="e8662f21ef0646a8abfab4f692e441ab"
    headers = {
        'Ocp-Apim-Subscription-Key': translator_key,
        'Content-type': 'application/json',
    }
    # Construct body
    body = [{"Text": text} for text in string_list]
    # Post request, return
    response = requests.post(url=base_url, headers=headers, json=body)
    # Extract translations
    return response.json()[0].get('language')

detect_language([message])