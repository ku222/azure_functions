
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


account_id = 'A00003088'

data = "{\r\n  \"Sports\": \"2700\",\r\n  \"Accomodation\": \"1300\",\r\n  \"Groceries\": \"1000\",\r\n  \"Utilities\": \"1000\",\r\n  \"Retail\": \"700\",\r\n  \"Travel\": \"700\",\r\n  \"Charity\": \"600\",\r\n  \"Medical\": \"600\",\r\n  \"Music\": \"600\",\r\n  \"Restaurant\": \"400\",\r\n  \"Employment\": \"300\",\r\n  \"Banking\": \"0\"\r\n}"

targets = json.loads(data)


def query_database(query):
    logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
    body = {"intent": "query", "params": [query]}
    response = requests.post(url=logic_app_url, json=body)
    return json.loads(response.content)

def delete_existing_targets(account_id):
    query = f"DELETE FROM [dbo].[CategoryBudget] WHERE account_id='{account_id}'"
    # execute
    query_database(query)

def insert_new_targets(targets, account_id):
    query = []
    for (category, target) in targets.items():
        target = float(target)
        query.append(f"('{account_id}', '{category}', {target})")
    final_query = "INSERT INTO [dbo].[CategoryBudget] VALUES " + ', '.join(query)
    # execute
    query_database(final_query)
        
        
# delete_existing_targets(account_id)
# insert_new_targets(targets, account_id)

