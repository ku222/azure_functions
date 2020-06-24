import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve params
    req_body = req.get_json()
    account_id = req_body.get('account_id')
    
    def query_database(query):
        logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
        body = {"intent": "query", "params": [query]}
        response = requests.post(url=logic_app_url, json=body)
        return json.loads(response.content)
    
    data = query_database(f"SELECT TOP 3 * FROM [dbo].[Card]")
    
    def display_cards(data):
        adaptive = AdaptiveCard()
        cards = data["ResultSets"]["Table1"]

        for card in cards:
            font_color = "default"
            backgroundImage_url = "https://i.dlpng.com/static/png/6774669_preview.png" if card["Status"]=="Frozen" else "https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg"
            
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
                                ActionSubmit(title="Reset PIN", data={"card": f"{card['card_id']}", "action": "PIN"}, style="positive"),
                                ActionSubmit(title="Defrost Card" if card["Status"]=="Frozen" else "Freeze Card",
                                            data={
                                                "card": f"{card['card_id']}",
                                                "action": f"{'unfreeze' if card['Status']=='Frozen' else 'freeze'}"
                                                }
                                            ,
                                            style="positive"),
            "^"
            ])
            
        return adaptive.to_json(version="1.1")
    
    result = display_cards(data)
    return func.HttpResponse(body=result, status_code=200)