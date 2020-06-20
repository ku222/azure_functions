import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve account number
    req_body = req.get_json()
   
    def create_card():
        card = AdaptiveCard()
        card.add(TextBlock(text=f"{chr(9608)*10}", weight="lighter", isSubtle="true"))
        return card.to_json()
    
    # Create card
    result = create_card()
    return func.HttpResponse(body=result, status_code=200)

#%%

