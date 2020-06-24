
#%%

import requests

DEPLOYED_URL = 'http://cloudwars2functionapp.azurewebsites.net/api/NavigationBranchFormatter?code=GMtryo1P7lJD3Jq4K7ILowWbTC/HKfM97dZ6bNLqdV3e9xgISHCftw=='

json_payload = {'address': 'Beverly Hills, 90210'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)


#%%

response.text


#%%

import requests
import json

def query_database(query):
    logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
    body = {"intent": "query", "params": [query]}
    response = requests.post(url=logic_app_url, json=body)
    return json.loads(response.content)

db_dict = query_database("SELECT Branch_ID FROM [dbo].[BranchWithGeo]")
branch_ids = [dict_['Branch_ID'] for dict_ in db_dict['ResultSets']['Table1']]


#%%

from collections import defaultdict
import random
from datetime import 

def generate_appointments(branch_ids):
    data = defaultdict(list)
    for branch_id in branch_ids:
        num_appointments = random.randint(0, 3)
           
#%%

u"\u2605"*4+u"\u2606"