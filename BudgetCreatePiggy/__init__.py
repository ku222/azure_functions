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
    account_id = req_body.get('account_id')
    language = req_body.get('language')
   
    def construct_create_piggybank_card(language):
        blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
        piggy_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Piggy_Bank_or_Savings_Flat_Icon_Vector.svg/1024px-Piggy_Bank_or_Savings_Flat_Icon_Vector.svg.png"

        # Initialize card
        card = AdaptiveCard(backgroundImage=blue_background)

        card.add([
            "items",
            TextBlock(text="Create a new Piggy Bank", color="light", size="Large", weight="Bolder", horizontalAlignment="center"),
            Image(url=piggy_icon, height="170px", horizontalAlignment="center"),
            
            # Add spacing
            Container(spacing="small"),
                "<",
            
            ColumnSet(),
                Column(width=1),
                    "<",
                Column(width=5),
                    TextBlock(text="Type in a name for your Piggy Bank", color="light", horizontalAlignment="center"),
                    InputText(ID="name", placeholder="Unique Name"),
                    TextBlock(text="E.g. Savings, Holiday, Rainy Day", color="light", size="small"),
                    ActionSet(separator="true", spacing="medium"),
                        "action",
                        ActionSubmit(title="Create", style="positive"),
                        ActionSubmit(title="Cancel", style="destructive", data={"action": "cancel"}),
                        "<",
                    "<",
                "item",
                Column(width=1),
                    "<",
        ])
        # Serialize to json
        return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")

    # Create card
    result = construct_create_piggybank_card(language)
    return func.HttpResponse(body=result, status_code=200)

