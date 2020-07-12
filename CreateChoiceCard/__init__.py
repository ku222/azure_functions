import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:

    req_body = req.get_json()
    prompts = req_body.get('prompts')
    actions = req_body.get('actions')
    language = req_body.get('language')
    
    def create_card(prompts, actions, language):
        blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
        card = AdaptiveCard(backgroundImage=blue_background)
        for (prompt, action) in zip(prompts, actions):
            card.add([
                "items",
                ActionSet(),
                    "action",
                    ActionSubmit(title=prompt, data={"action": action}),
            "^"
            ])
        
        if language == 'en':
            return card.to_json()
        return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")
        
    result = create_card(prompts, actions, language)
    return func.HttpResponse(body=result, status_code=200)

