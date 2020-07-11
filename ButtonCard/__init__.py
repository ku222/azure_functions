import logging
import azure.functions as func
import json
from adaptivecardbuilder import *

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    prompt = req_body.get('prompt')
    placeholder = req_body.get('placeholder')
    submit_title = req_body.get('submit_title')
    language = req_body.get('language')
    
    def create_card(prompt, placeholder, submit_title, language):
        card = AdaptiveCard()
        
        card.add([
            "items",
            TextBlock(text=prompt, weight="Bolder", separator="true"),
            InputText(ID="input", placeholder=placeholder),
            
            "Actions",
            ActionSubmit(title=submit_title)
        ])
                        
        return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")
    
    result = create_card(prompt, placeholder, submit_title, language)
    return func.HttpResponse(body=result, status_code=200)