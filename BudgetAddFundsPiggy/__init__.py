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
    piggybank_name = req_body.get('piggybank_name')
    
    def query_database(query):
        logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
        body = {"intent": "query", "params": [query]}
        response = requests.post(url=logic_app_url, json=body)
        return json.loads(response.content)
   
    # Retrieve account balance
    db_dict = query_database(f"SELECT balance from [dbo].[Profile] WHERE account_id = '{account_id}'")
    balance = db_dict['ResultSets']['Table1'][0]['balance']
   
    def create_addfunds_card(balance, piggybank_name):
        blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
        piggy_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Piggy_Bank_or_Savings_Flat_Icon_Vector.svg/1024px-Piggy_Bank_or_Savings_Flat_Icon_Vector.svg.png"
        coin_icon = "https://i.ibb.co/7pSTx1L/coin.png"
        
        # Initialize card
        card = AdaptiveCard(backgroundImage=blue_background)

        # Add card elements
        card.add([
            TextBlock(text=f"Add to your {piggybank_name} Piggy Bank", color="light", size="Large", weight="Bolder", horizontalAlignment="center"),
            TextBlock(text=f"Account Balance: ${balance:,}", color="light", weight="bolder", size="medium", horizontalAlignment="center"),
            ColumnSet(),
                Column(),
                    Container(spacing="small"), "<",
                    Container(spacing="medium"), "<",
                    Image(url=coin_icon, height="100px", horizontalAlignment="center"),
                    "<",
                Column(),
                    Image(url=piggy_icon, height="140px", horizontalAlignment="center"),
                    "<",
                "<",
            
            TextBlock(text="Type in an amount to add", horizontalAlignment="center", color="light"),
            ColumnSet(),
                Column(width=1),
                    TextBlock(text="$", color="light", size="Large", verticalAlignment="center", horizontalAlignment="right"),
                    "<",
                Column(width=5),
                    InputNumber(ID="amount", placeholder="50.00"),
                    ActionSet(separator="true", spacing="medium"),
                        "action",
                        ActionSubmit(title="Add Funds!", style="positive"),
                        "<",
                    "<",
                "items",
                Column(width=1),
                    "<",
                "<"
        ])
        # Serialize to json
        return card.to_json()

    # Create card
    result = create_addfunds_card(balance, piggybank_name)
    return func.HttpResponse(body=result, status_code=200)

