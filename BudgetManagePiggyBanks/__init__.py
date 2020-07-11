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
    
    def query_database(query):
        logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
        body = {"intent": "query", "params": [query]}
        response = requests.post(url=logic_app_url, json=body)
        return json.loads(response.content)

    # Retrieve piggybank list
    db_dict = query_database(f"SELECT * from [dbo].[Piggybank] WHERE account_id = '{account_id}'")
    piggybank_list = db_dict["ResultSets"]["Table1"]
    
    def create_piggybanks(piggybank_list, language):
        blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
        piggy_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Piggy_Bank_or_Savings_Flat_Icon_Vector.svg/1024px-Piggy_Bank_or_Savings_Flat_Icon_Vector.svg.png"
        # Initailize card
        card = AdaptiveCard()
        
        for piggy_dict in piggybank_list:
            piggybank_name = piggy_dict["piggybank_name"]
            amount = piggy_dict["amount"]
            created_date = piggy_dict["created_date"].split('T')[0]
            monthly_allowance = piggy_dict["monthly_allowance"]
            # add to card
            card.add(Container(backgroundImage=blue_background))
            card.add(TextBlock(text=piggybank_name, color="light", size="Large", weight="Bolder", horizontalAlignment="center", dont_translate=True))
            card.add(TextBlock(text=f"Amount: ${amount:,}", color="light", size="medium", horizontalAlignment="center"))
            card.add(TextBlock(text=f"Born: {created_date}", color="light", size="medium", horizontalAlignment="center"))
            if monthly_allowance > 0:
                card.add(TextBlock(text=f"Monthly allowance: ${monthly_allowance:,}", color="light", size="medium", horizontalAlignment="center"))
            card.add(Image(url=piggy_icon, height="170px", horizontalAlignment="center"))
            card.add(ActionSet(separator="true", spacing="medium"))
            card.add(ActionSubmit(title="Add to Piggy Bank", style="positive", data={"action": "add", "piggybank_name": piggybank_name}), is_action=True)
            card.add(ActionSubmit(title="Change Monthly Allowance", style="positive", data={"action": "change_allowance", "piggybank_name": piggybank_name}), is_action=True)
            card.add(ActionSubmit(title="Smash Piggy Bank", style="destructive", data={"action": "smash", "piggybank_name": piggybank_name}), is_action=True)
            card.back_to_top()        
        
        return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")
            
    # Create card
    result = create_piggybanks(piggybank_list, language)
    return func.HttpResponse(body=result, status_code=200)

