import logging
import azure.functions as func
import json
from adaptivecardbuilder import *

def main(req: func.HttpRequest) -> func.HttpResponse:

    req_body = req.get_json()
    prompt = req_body.get('prompt')
    placeholder = req_body.get('placeholder')
    submit_title = req_body.get('submit_title')
    language = req_body.get('language')
    
    def create_card(prompt, placeholder, submit_title, language):
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
                        
        return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")
    
    result = create_card(prompt, placeholder, submit_title, language)
    return func.HttpResponse(body=result, status_code=200)