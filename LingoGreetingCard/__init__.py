import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    def create_welcome_card():
        # Create card
        blue_background = "https://images.unsplash.com/photo-1557683311-eac922347aa1?ixlib=rb-1.2.1&w=1000&q=80"
        bot_icon = "https://i.ibb.co/dmmWb6s/Lingo-Bot-Bare.png"

        card = AdaptiveCard(backgroundImage=blue_background)
        card.add([
            Container(),
                "<",
            Image(url=bot_icon, spacing="medium", height="130px", horizontalAlignment="center"),
            TextBlock(text=f"Hey! I'm Lingo", spacing="Large", weight="bolder", size="ExtraLarge", horizontalAlignment="center", color="light"),
            TextBlock(text="Your Personal Digital Banking Assistant", weight="bolder", size="Large", horizontalAlignment="center", wrap="true", color="light"),
            TextBlock(text="I can speak more than 70 languages!", weight="bolder", size="Medium", horizontalAlignment="center", wrap="true", color="light"),
            ActionSet(spacing="Large"),
                "action",
                ActionSubmit(title="Help", data={"action": "help"}, iconUrl="https://img.icons8.com/ios/50/000000/help.png")
        ])
        return card.to_json()

    result = create_welcome_card()
    return func.HttpResponse(body=result, status_code=200)


