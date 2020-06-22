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
   
    def query_database(query):
        logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
        body = {"intent": "query", "params": [query]}
        response = requests.post(url=logic_app_url, json=body)
        return json.loads(response.content)
    
    # Retrieve amount and created date of the piggybank in question from the piggybank table
    db_dict = query_database(f"SELECT amount, created_date from [dbo].[PiggyBank] WHERE account_id = '{account_id}' AND piggybank_name = '{piggybank_name}'")
    amount = db_dict['ResultSets']['Table1'][0]['amount']
    created_date = db_dict['ResultSets']['Table1'][0]['created_date'].split('T')[0]
    date_today = str(date.today())

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
        # Add into normal transaction table
        query = f"INSERT INTO [dbo].[Transaction] VALUES ('{trn_no}', '{account_id}', {date_today}, '{transaction_details}', NULL, {date_today}, {0 if operator=='-' else amount}, {amount if operator=='-' else 0}, {new_balance})"
        query_database(query)
        # Add into category transaction table
        query = f"INSERT INTO [dbo].[Transaction_with_category] VALUES ('{trn_no}', '{account_id}', {date_today}, '{transaction_details}', NULL, {date_today}, {0 if operator=='-' else amount}, {amount if operator=='-' else 0}, {new_balance}, 'BANKING', 'COMPLETE')"
        query_database(query)
        
    def delete_piggybank(account_id, piggybank_name):
        query = f"DELETE FROM [dbo].[PiggyBank] WHERE account_id = '{account_id}' AND piggybank_name = '{piggybank_name}'"
        query_database(query)
   
    def create_card(piggybank_name, piggybank_amount, created_date, date_today):
        blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
        piggy_icon = "https://i.ibb.co/sKfW8Nd/debt.png"

        card = AdaptiveCard(backgroundImage=blue_background)
        card.add([
            TextBlock(text=f"Here lies", color="light", size="ExtraLarge", weight="Bolder", horizontalAlignment="center"),
            TextBlock(text=f"Good Old {piggybank_name} Piggy Bank", color="light", size="Large", wrap="true", horizontalAlignment="center"),
            TextBlock(text=f"Who Amounted to ${piggybank_amount:,}", color="light", size="Medium", wrap="true", horizontalAlignment="center"),
            
            ColumnSet(separator="true", spacing="Large"),
                Column(),
                    TextBlock(text=f"Born", color="light", separator="true", size="Large", weight="bolder", spacing="Large", wrap="true", horizontalAlignment="center"),
                    TextBlock(text=f"{created_date}", color="light", size="Large", wrap="true", horizontalAlignment="center"),
                    "<",
                Column(),
                    TextBlock(text=f"Smashed", color="light", size="Large", weight="bolder", spacing="Large", wrap="true", horizontalAlignment="center"),
                    TextBlock(text=f"{date_today}", color="light", size="Large", wrap="true", horizontalAlignment="center"),
                    "<",
                "<",
            
            Image(url=piggy_icon, spacing="Large", height="200px", horizontalAlignment="center"),
            
        ])
        return card.to_json()
    
    # Delete piggybank from database
    delete_piggybank(account_id=account_id, piggybank_name=piggybank_name)

    # Update necessary tables to reflect this - operator is "-" because we're subtracting from their account
    update_balance_and_transactions(account_id=account_id, amount=float(amount), transaction_details=f"Smashed Piggy Bank {piggybank_name}", operator="+")
    
    # Create card
    result = create_card(piggybank_name=piggybank_name, piggybank_amount=float(amount), created_date=created_date, date_today=date_today)
    return func.HttpResponse(body=result, status_code=200)

