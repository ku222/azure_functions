
#%%

import requests
import json

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/ViewProfile?code=pa7gOnUTxIPwEeN13gHpeN4gqgkg9agdZZh/XTjC2ABquysNfZDYLQ=='
json_payload = {"account_id": 'A00000001'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%% Example payload in dict form

from adaptivecardbuilder import *
import requests
import json

account_id = 'A00000001'


def query_database(query):
    logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
    body = {"intent": "query", "params": [query]}
    response = requests.post(url=logic_app_url, json=body)
    return json.loads(response.content)

def display_profile(data):
    # Dict mapping database names to pretty names
    DB_TO_CARD = {
    'sex': 'Sex',
    'fulldate': 'Date of Birth',
    'social': 'Social Security Number',
    'first': 'First Name',
    'middle': 'Middle Name',
    'last': 'Last Name',
    'phone': 'Phone Number',
    'address_1': 'Address Line 1',
    'address_2': 'Address Line 2',
    'city': 'City',
    'state': 'State',
    'zipcode': 'Zip Code',
    'job': 'Occupation',
    'marital': 'Marital Status',
    'education': 'Highest Education',
    'contact': 'Contact Type',
    'email': 'Email Address'
    }
    
    # Remove any unneeded keys
    profile_dict = {k:v for (k,v) in data.items() if k in DB_TO_CARD}
    
    # Rearrange keys so name ones are first, then all others after
    name_keys = ("first", "middle", "last")
    names_dict = {k:v for (k,v) in profile_dict.items() if k in name_keys}
    non_names_dict = {k:v for (k,v) in profile_dict.items() if k not in name_keys}
    names_dict.update(non_names_dict)
    profile_dict = names_dict
    
    # Initialize card
    card = AdaptiveCard()
    for (raw_field_name, current_value) in profile_dict.items():
        # prettify name
        pretty_name = DB_TO_CARD.get(raw_field_name)
        # prettify current value
        if type(current_value) == str:
            current_value = current_value.title()
        # clean up date if its a date
        if pretty_name == "Date of Birth":
            current_value = current_value.split('T')[0]
        # add to card
        card.add([
            "items-------",
            Container(spacing="medium", separator="true"),
                ColumnSet(),
                    Column(),
                        TextBlock(text=pretty_name, weight="Bolder"),
                        "<",
                    Column(),
                        TextBlock(text=current_value, isSubtle="true"),
            "^"
        ])

        # Return to main body again
        card.back_to_top()
        
    # Finish by adding update action button
    card.add(Container(spacing="ExtraLarge", separator="true"))
    card.up_one_level()
    card.add(ActionSubmit(title="Update Profile", data={"action": "update"}), is_action=True)
    
    return card.to_json()

# Retrieve account data from database
db_response = query_database(f"SELECT * FROM [dbo].[Profile] WHERE account_id = '{account_id}'")
data = db_response["ResultSets"]["Table1"][0]

# Create card
result = display_profile(data)