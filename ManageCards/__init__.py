import logging
import azure.functions as func
import json
from adaptivecardbuilder import *

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve intent, data
    intent = req.params.get('intent')
    data = req.params.get('data')
    
    # general error handler - taken from example documentation
    if not intent:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            intent = req_body.get('intent')
       
    if not data:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            data = req_body.get('data')
            
    if not intent:
        return func.HttpResponse(body='Intent missing', status_code=400)
    
    if not data:
        return func.HttpResponse(body='Data missing', status_code=400)
    
    # Serialize our data into a python dict
    data = json.loads(data)
        
    def display_cards(data):
        adaptive = AdaptiveCard()
        cards = data["ResultSets"]["Table1"]

        for card in cards:
            font_color = "default"
            backgroundImage_url = "https://i.dlpng.com/static/png/6774669_preview.png" if card["Status"]=="Frozen" else "https://www.publicdomainpictures.net/pictures/30000/velka/plain-white-background.jpg"
            
            adaptive.add([
                "items----",
                Container(backgroundImage=backgroundImage_url, spacing="large", separator="true"),
                    ColumnSet(),
                        Column(),
                            TextBlock(text=card["card_id"], color=font_color),
                            TextBlock(text=card["type"], size="ExtraLarge", weight="Bolder", color=font_color),
                            TextBlock(text=f"Status: {card['Status']}", size="medium", weight="Bolder", color=font_color),
                            TextBlock(text=f"Expires {card['month']}-{card['day']}-{card['year']}", color=font_color),
                            TextBlock(text=f"PIN: {card['Pin_Code']}", color=font_color),
                            "<",
                        Column(),
                            Image(url="https://brokerchooser.com/uploads/images/digital-banks/n26-review-bank-card.png"),
                            "<",
                        "<",
                        
                    ActionSet(),
                        "actions ----",
                        ActionShowCard(title="Manage Card"),
                            ActionSubmit(title="Reset PIN", data={"card": f"{card['card_id']}", "action": "PIN"}),
                            ActionSubmit(title="Defrost Card" if card["Status"]=="Frozen" else "Freeze Card",
                                        data={
                                            "card": f"{card['card_id']}",
                                            "action": f"{'unfreeze' if card['Status']=='Frozen' else 'freeze'}"
                                            }
                                        ),
            "^"
            ])
            
        return adaptive.to_json()
    
    result = display_cards(data)
    return func.HttpResponse(body=result, status_code=200)