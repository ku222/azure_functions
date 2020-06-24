import logging
import azure.functions as func
import json
from adaptivecardbuilder import *

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve parameters
    prompt = req.params.get('prompt')
    placeholder = req.params.get('placeholder')
    submit_title = req.params.get('submit_title')
    
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        prompt = req_body.get('prompt')
        placeholder = req_body.get('placeholder')
        submit_title = req_body.get('submit_title')
       
    if not prompt or not placeholder or not submit_title:
        return func.HttpResponse(body='One or more parameters missing', status_code=400)
    
    def create_card(prompt, placeholder, submit_title):
        card = AdaptiveCard(backgroundImage="https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png")
        
        card.add([
            "items",
            Container(backgroundImage="https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg"),
                TextBlock(text=prompt, weight="Bolder", separator="true"),
                InputText(ID="input", placeholder=placeholder),
                "<",
        
            "Actions",
            ActionSubmit(title=submit_title, style="positive")
        ])
                        
        return card.to_json()
    
    result = create_card(prompt, placeholder, submit_title)
    return func.HttpResponse(body=result, status_code=200)