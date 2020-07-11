import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests
from datetime import date
import random

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve account number
    req_body = req.get_json()
    account_id = req_body.get('account_id')
    piggybank_name = req_body.get('piggybank_name')
    amount = req_body.get('amount')
    language = req_body.get('language')
   
    def query_database(query):
        logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
        body = {"intent": "query", "params": [query]}
        response = requests.post(url=logic_app_url, json=body)
        return json.loads(response.content)

    def update_balance_and_transactions(account_id, amount, transaction_details, operator="-"):
        # Retrieve account balance
        db_dict = query_database(f"SELECT balance from [dbo].[Profile] WHERE account_id = '{account_id}'")
        balance = db_dict['ResultSets']['Table1'][0]['balance']
        # Calculate new balance
        if operator == "-":
            new_balance = balance - amount
        elif operator == "+":
            new_balance = balance + amount
        # First update balance in profile
        query = f"UPDATE [dbo].[Profile] SET balance = {new_balance} WHERE account_id = '{account_id}'"
        query_database(query)
        # Now record a transaction
        date_today = "CURRENT_TIMESTAMP"
        trn_no = 'PIG' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=10))
        # Add into category transaction table
        query = f"INSERT INTO [dbo].[Transaction_with_category] VALUES ('{trn_no}', '{account_id}', {date_today}, '{transaction_details}', NULL, {date_today}, {0 if operator=='-' else amount}, {amount if operator=='-' else 0}, {new_balance}, 'BANKING', 'COMPLETE', 'BOT')"
        query_database(query)
        
    def insert_piggybank(account_id, piggybank_name, amount):
        date_today = "CURRENT_TIMESTAMP"
        query = f"INSERT INTO [dbo].[Piggybank] VALUES ('{account_id}', '{piggybank_name}', {amount}, {date_today}, {0})"
        # execute
        query_database(query)
   
    def create_finish_card(piggybank_name, amount, language):
        blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
        piggy_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Piggy_Bank_or_Savings_Flat_Icon_Vector.svg/1024px-Piggy_Bank_or_Savings_Flat_Icon_Vector.svg.png"

        card = AdaptiveCard(backgroundImage=blue_background)

        card.add([
            "items",
            TextBlock(text="All done!", color="light", size="Large", weight="Bolder", horizontalAlignment="center"),
            TextBlock(text=f"Your new Piggy Bank is now set up. Happy saving!", color="light", wrap="true", size="Medium", horizontalAlignment="center"),
            Container(spacing="medium"), "<",
            TextBlock(text=piggybank_name, color="light", size="Large", horizontalAlignment="center", dont_translate=True),
            TextBlock(text=f"${float(amount):,}", color="light", size="Large", weight="Bolder", horizontalAlignment="center", dont_translate=True),
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
                        ActionSubmit(title="View all Piggy Banks", style="positive", data={"action": "view"}),
                        ActionSubmit(title="Pay Myself an Allowance from This", style="positive", data={"action": "monthly_allowance"}),
                        "<",
                    "<",
                "item",
                Column(width=1),
                    "<",
        ])
        # Serialize
        return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")

    # Insert new piggybank into database
    insert_piggybank(account_id, piggybank_name, amount)

    # Update necessary tables to reflect this - operator is "-" because we're subtracting from their account
    update_balance_and_transactions(account_id=account_id, amount=float(amount), transaction_details=f"New Piggy Bank {piggybank_name}", operator="-")
    
    # Create card
    result = create_finish_card(piggybank_name, amount, language)
    return func.HttpResponse(body=result, status_code=200)

