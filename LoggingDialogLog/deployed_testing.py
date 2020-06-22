
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
dialog_name = "ManageProfile"
dialog_unique_id = '8426830516534674385267'
dialog_start_or_end = 'end'
activity = "{\r\n  \"type\": \"message\",\r\n  \"id\": \"8c5199f0-b3fc-11ea-b28a-d9c1322bbac3\",\r\n  \"timestamp\": \"2020-06-21T21:19:45.551+01:00\",\r\n  \"localTimestamp\": \"2020-06-21T21:19:45+01:00\",\r\n  \"serviceUrl\": \"https://11d80383dacb.ngrok.io\",\r\n  \"channelId\": \"emulator\",\r\n  \"from\": {\r\n    \"id\": \"5a30351c-39a7-4582-9d70-e7f6f0d33e77\",\r\n    \"name\": \"User\",\r\n    \"role\": \"user\"\r\n  },\r\n  \"conversation\": {\r\n    \"id\": \"85f09b10-b3fc-11ea-b28a-d9c1322bbac3|livechat\"\r\n  },\r\n  \"recipient\": {\r\n    \"id\": \"85ed8dd0-b3fc-11ea-a096-777abc2220db\",\r\n    \"name\": \"Bot\",\r\n    \"role\": \"bot\"\r\n  },\r\n  \"textFormat\": \"plain\",\r\n  \"locale\": \"en-US\",\r\n  \"text\": \"manage my profile\",\r\n  \"channelData\": {\r\n    \"clientActivityID\": \"1592770785549qah9rjjuz9\",\r\n    \"clientTimestamp\": \"2020-06-21T20:19:45.549Z\"\r\n  },\r\n  \"callerId\": \"urn:botframework:azure\"\r\n}"
activity_dict = json.loads(activity)

def query_database(query):
    logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
    body = {"intent": "query", "params": [query]}
    response = requests.post(url=logic_app_url, json=body)
    return json.loads(response.content)

def preprocess_insert_data(account_id, dialog_name, dialog_unique_id, dialog_start_or_end, activity_dict):
    dialog_log_fields = ['account_id', 'dialog_name', 'dialog_unique_id', 'dialog_start_time', 'dialog_end_time', 
                            'user_id', 'conversation_id', 'channel_client_activity_id']
    
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
    output['text'] = activity_dict.get('text')
    
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
    #query_database(insert_query)
    print(insert_query)
    
# Else we simply update the existing entry's dialog end time
elif dialog_start_or_end.lower() == 'end':
    dialog_end_time = activity_dict.get('timestamp').split('+')[0]
    update_query = f"UPDATE [dbo].[DialogLog] SET dialog_end_time = '{dialog_end_time}' WHERE dialog_unique_id = 'd-{dialog_unique_id}'"
    #query_database(update_query)
    print(update_query)
    

#%%
    
