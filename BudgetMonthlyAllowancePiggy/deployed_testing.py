
#%%

import requests
import json

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/BudgetMonthlyAllowancePiggy?code=LvJ6nbVoR3V09C4LazQWhOEI2xjqyqeablfjrE/a08GTpQ/WlbfqzA=='
json_payload = {"account_id": 'A00003088', "piggybank_name": "Mortgage"}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%% Example payload in dict form
# u'\u2588'

from adaptivecardbuilder import *
import requests
import json


account_id = "A00003088"
piggybank_name = "Mortgage"


#%%
def query_database(query):
    logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
    body = {"intent": "query", "params": [query]}
    response = requests.post(url=logic_app_url, json=body)
    return json.loads(response.content)

# Retrieve account balance
db_dict = query_database(f"SELECT balance from [dbo].[Profile] WHERE account_id = '{account_id}'")
balance = db_dict['ResultSets']['Table1'][0]['balance']

#%%

db_dict = query_database(f"SELECT monthly_allowance from [dbo].[PiggyBank] WHERE account_id = '{account_id}' AND piggybank_name = '{piggybank_name}'")
monthly_allowance = db_dict['ResultSets']['Table1'][0]['monthly_allowance']

#%%

monthly_allowance