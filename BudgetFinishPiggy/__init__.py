import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests
from datetime import date

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve account number
    req_body = req.get_json()
    account_id = req_body.get('account_id')
    piggybank_name = req_body.get('piggybank_name')
    amount = req_body.get('amount')
   
    def query_database(query):
        logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
        body = {"intent": "query", "params": [query]}
        response = requests.post(url=logic_app_url, json=body)
        return json.loads(response.content)

    def insert_piggybank(account_id, piggybank_name, amount):
        date_today = str(date.today())
        query = f"INSERT INTO [dbo].[Piggybank] VALUES ('{account_id}', '{piggybank_name}', {amount}, '{date_today}', {0})"
        # execute
        query_database(query)
   
    def create_finish_card(piggybank_name, amount):
        blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
        piggy_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Piggy_Bank_or_Savings_Flat_Icon_Vector.svg/1024px-Piggy_Bank_or_Savings_Flat_Icon_Vector.svg.png"

        card = AdaptiveCard(backgroundImage=blue_background)

        card.add([
            "items",
            TextBlock(text="All done!", color="light", size="Large", weight="Bolder", horizontalAlignment="center"),
            TextBlock(text=f"Your new Piggy Bank is now set up. Happy saving!", color="light", wrap="true", size="Medium", horizontalAlignment="center"),
            Container(spacing="medium"), "<",
            TextBlock(text=piggybank_name, color="light", size="Large", horizontalAlignment="center"),
            TextBlock(text=f"${float(amount):,}", color="light", size="Large", weight="Bolder", horizontalAlignment="center"),
            Image(url=piggy_icon, height="120px", horizontalAlignment="center"),
            
            # Add spacing
            Container(spacing="small"),
                "<",
            
            ColumnSet(),
                Column(width=1),
                    "<",
                Column(width=5),
                    Container(), "<",
                    ActionSet(separator="true", spacing="medium"),
                        "action",
                        ActionSubmit(title="View all PiggyBanks", style="positive", data={"action": "view"}),
                        ActionSubmit(title="Pay Myself an Allowance from This", style="positive", data={"action": "monthly_allowance"}),
                        "<",
                    "<",
                "item",
                Column(width=1),
                    "<",
        ])
        # Serialize
        return card.to_json()

    # Insert new piggybank into database
    insert_piggybank(account_id, piggybank_name, amount)
    
    # Create card
    result = create_finish_card(piggybank_name, amount)
    return func.HttpResponse(body=result, status_code=200)
