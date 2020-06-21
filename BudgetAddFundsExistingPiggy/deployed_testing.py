
#%%

import requests
import json

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/ViewProfile?code=pa7gOnUTxIPwEeN13gHpeN4gqgkg9agdZZh/XTjC2ABquysNfZDYLQ=='
json_payload = {"account_id": 'A00000001'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%% Example payload in dict form
# u'\u2588'

from adaptivecardbuilder import *
import requests
import json
from datetime import date
import random

account_id = 'A00003088'
piggybank_name = "Holiday"
amount = float("100")

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
    date_today = str(date.today())
    trn_no = 'PIG' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=10))
    # Add into normal transaction table
    query = f"INSERT INTO [dbo].[Transaction] VALUES ('{trn_no}', '{account_id}', '{date_today}', '{transaction_details}', NULL, '{date_today}', {0 if operator=='-' else amount}, {amount if operator=='-' else 0}, {new_balance})"
    query_database(query)
    # Add into category transaction table
    query = f"INSERT INTO [dbo].[Transaction_with_category] VALUES ('{trn_no}', '{account_id}', '{date_today}', '{transaction_details}', NULL, '{date_today}', {0 if operator=='-' else amount}, {amount if operator=='-' else 0}, {new_balance}, 'BANKING', 'COMPLETE')"
    query_database(query)
    