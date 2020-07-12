import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:

    req_body = req.get_json()
    message = req_body.get('message')
   
    app_id = "9117b808-1323-4b13-aed4-47d4b6fa6a04"
    authoring_key = "f941aa60cf67403fa1b7a528a613993b"
    endpoint = "https://westeurope.api.cognitive.microsoft.com"
    parameters = {
        'query': message,
        'timezoneOffset': '0',
        'verbose': 'true',
        'show-all-intents': 'true',
        'spellCheck': 'false',
        'staging': 'false',
        'subscription-key': authoring_key
    }
    response = requests.get(f"{endpoint}/luis/prediction/v3.0/apps/{app_id}/slots/production/predict", params=parameters)
    top_intent = response.json().get('prediction').get('topIntent')
    
    return func.HttpResponse(body=top_intent, status_code=200)



#%%

