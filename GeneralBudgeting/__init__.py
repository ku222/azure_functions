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
    language = req_body.get('language')
   
    def create_card(language):
        card = AdaptiveCard()
        card.add([
            "items",
            Container(backgroundImage="https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"),
                TextBlock(text="Lingfield Piggy Banks", color="light", size="ExtraLarge", weight="Bolder", spacing="ExtraLarge", horizontalAlignment="center"),
                Image(url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Piggy_Bank_or_Savings_Flat_Icon_Vector.svg/1024px-Piggy_Bank_or_Savings_Flat_Icon_Vector.svg.png", height="170px", horizontalAlignment="center"),
                TextBlock(text="Set money aside for bills, fees, or a rainy day", wrap="true", color="light", horizontalAlignment="center", size="medium", separator="true"),
                ActionSet(spacing="small"),
                    "action",
                    ActionShowCard(title="Learn More"),
                        "items",
                        Container(backgroundImage="https://www.publicdomainpictures.net/pictures/30000/velka/plain-white-background.jpg"),
                            TextBlock(text="Lingfield Piggy Banks are a great way to set money aside, away from your main balance.", wrap="true"),
                            TextBlock(text="You could try putting the money you need for bills into a pot as soon as you get paid, and only moving it back into your account when you need it.", wrap="true"),
                            TextBlock(text="This means you can set aside everything you need to spend on bills, rent or mortgage payments safely, so you do not spend it accidentally!", wrap="true"),
                            ActionSet(),
                                "action",
                                ActionSubmit(title="Create a new Piggy Bank", style="positive", data={"action": "piggy"}),
        ])
        
        # Go back to top
        card.back_to_top()
        
        # Next batch - category budgets
        card.add([
            "items",
            Container(backgroundImage="https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"),
                TextBlock(text="Personal (Financial) Trainer", color="light", size="ExtraLarge", weight="Bolder", spacing="ExtraLarge", horizontalAlignment="center"),
                Image(url="https://i.ibb.co/vH4BM82/referee.png", height="120px", horizontalAlignment="center"),
                TextBlock(text="Get tough on your budgeting with monthly goals", wrap="true", color="light", horizontalAlignment="center", size="medium", separator="true", spacing="large"),
                ActionSet(spacing="small"),
                    "action",
                    ActionShowCard(title="Learn More"),
                        "items",
                        Container(backgroundImage="https://www.publicdomainpictures.net/pictures/30000/velka/plain-white-background.jpg"),
                            TextBlock(text="Enlist your very own personal financial trainer to get your budgeting into shape!", wrap="true"),
                            TextBlock(text="Set monthly spending budgets for each category of spending, helping you reach your saving goals.", wrap="true"),
                            TextBlock(text="As you spend, we'll let you know how close you are getting to your spending limit for each category.", wrap="true"),
                            TextBlock(text="We won't stop you from spending over these limits - but it's a gentle reminder to stay on track.", wrap="true"),
                            ActionSet(),
                                "action",
                                ActionSubmit(title="Create a Budgeting Plan!", style="positive", data={"action": "budget"}),
        ])
        
        return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")

    result = create_card(language)
    return func.HttpResponse(body=result, status_code=200)