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
    targets = req_body.get('targets')

    # serialize to json
    targets = json.loads(targets)
    
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
        
    # Delete existing    
    delete_existing_targets(account_id)
    
    # Add new targets
    insert_new_targets(targets, account_id)
   
    result = 'done'
    return func.HttpResponse(body=result, status_code=200)


