import datetime
import logging

import json
import requests
import random

import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    
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
        # Add into normal transaction table
        query = f"INSERT INTO [dbo].[Transaction] VALUES ('{trn_no}', '{account_id}', {date_today}, '{transaction_details}', NULL, {date_today}, {0 if operator=='-' else amount}, {amount if operator=='-' else 0}, {new_balance})"
        query_database(query)
        # Add into category transaction table
        query = f"INSERT INTO [dbo].[Transaction_with_category] VALUES ('{trn_no}', '{account_id}', {date_today}, '{transaction_details}', NULL, {date_today}, {0 if operator=='-' else amount}, {amount if operator=='-' else 0}, {new_balance}, 'BANKING', 'COMPLETE')"
        query_database(query)
        
    db_dict = query_database(f"SELECT * FROM [dbo].[PiggyBank] WHERE amount > 0 AND monthly_allowance > 0")
    piggybank_dict_array = db_dict.get('ResultSets').get('Table1')

    for piggybank_dict in piggybank_dict_array:
        account_id = piggybank_dict.get('account_id')
        piggybank_name = piggybank_dict.get('piggybank_name')
        amount = piggybank_dict.get('amount')
        allowance = piggybank_dict.get('monthly_allowance')
        
        amount_to_transfer = min(allowance, amount)
        if amount_to_transfer > 0:
            update_query = f"UPDATE [dbo].[PiggyBank] SET amount=amount - {amount_to_transfer} WHERE account_id='{account_id}' AND piggybank_name='{piggybank_name}'"
            query_database(update_query)
            update_balance_and_transactions(account_id=account_id,
                                             amount=amount_to_transfer,
                                             transaction_details=f"Monthly allowance from Piggy Bank {piggybank_name}",
                                             operator="+")
            