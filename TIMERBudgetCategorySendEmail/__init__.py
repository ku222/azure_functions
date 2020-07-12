import logging
import json
import azure.functions as func
import requests
from collections import defaultdict

def main(req: func.HttpRequest, sendGridMessage: func.Out[str]) -> func.HttpResponse:

    req_body = req.get_json()
    email = req_body.get('email')
    email_body = req_body.get('email_body')

    message = {
        "personalizations": [ {
        "to": [{
            "email": email
            }]}],
        "subject": "Reminder from Bank of Lingfield!",
        "content": [{
            "type": "text/plain",
            "value": email_body}]}

    sendGridMessage.set(json.dumps(message))

    return func.HttpResponse(f"Sent")