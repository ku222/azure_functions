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

    # Retrieve relevant fields
    req_body = req.get_json()
    account_id = req_body.get('account_id')
    dialog_name = req_body.get('dialog_name')
    dialog_unique_id = req_body.get('dialog_unique_id')
    dialog_start_or_end = req_body.get('dialog_start_or_end')
    activity = req_body.get('activity')
    
    # Deserialize activity json
    activity_dict = json.loads(activity)

    def query_database(query):
        logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
        body = {"intent": "query", "params": [query]}
        response = requests.post(url=logic_app_url, json=body)
        return json.loads(response.content)

    def preprocess_insert_data(account_id, dialog_name, dialog_unique_id, dialog_start_or_end, activity_dict):      
        # Initialize blank output_dict
        output = dict()
        
        # Fill in fields from inputs
        output['account_id'] = account_id
        output['dialog_name'] = dialog_name
        output['dialog_unique_id'] = f"d-{dialog_unique_id}"
        
        # Timestamp formatting - remove the +XX:XX UTC offset bit
        output['dialog_start_time'] = activity_dict.get('timestamp').split('+')[0]
        output['dialog_end_time'] = None

        # Try get user IDs from both from and to portions
        from_dict = activity_dict.get('from')
        to_dict = activity_dict.get('recipient')
        user_id = ''
        if from_dict.get('role') == 'user':
            user_id = from_dict.get('id')
        if to_dict.get('role') == 'user':
            user_id = to_dict.get('id')
            
        # Add user ID to output dict
        output['user_id'] = user_id
        
        # Error handle conversation dict
        conversation_dict = activity_dict.get('conversation')
        if conversation_dict:
            output['conversation_id'] = conversation_dict.get('id')
        
        # Error handle channel dict
        channel_dict = activity_dict.get('channelData')
        if channel_dict:
            output['channel_client_activity_id'] = channel_dict.get('clientActivityID')
            
        return output

    def construct_insert_query(preprocessed_data):
        col_names = [k for k in preprocessed_data.keys()]
        value_names = [f"'{v}'"  if v else 'NULL' for v in preprocessed_data.values()]
        return f"INSERT INTO [dbo].[DialogLog] ({', '.join(col_names)}) VALUES ({', '.join(value_names)})"

    # Add new entry if its a start log
    if dialog_start_or_end.lower() == 'start':
        # Preprocess data
        preprocessed_data = preprocess_insert_data(account_id, dialog_name, dialog_unique_id, dialog_start_or_end, activity_dict)
        # Construct query from preprocessed data
        insert_query = construct_insert_query(preprocessed_data)
        # Execute query (log data to the Dialog-Log table)
        query_database(insert_query)
        
    # Else we simply update the existing entry's dialog end time
    elif dialog_start_or_end.lower() == 'end':
        dialog_end_time = activity_dict.get('timestamp').split('+')[0]
        update_query = f"UPDATE [dbo].[DialogLog] SET dialog_end_time = '{dialog_end_time}' WHERE dialog_unique_id = 'd-{dialog_unique_id}'"
        query_database(update_query)
    
    return func.HttpResponse(body='logged', status_code=200)

