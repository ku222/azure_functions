import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    account_id = req_body.get('account_id')
            
    if not account_id:
        return func.HttpResponse(body='Account ID missing', status_code=400)
    
    def query_database(query):
        logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
        body = {"intent": "query", "params": [query]}
        response = requests.post(url=logic_app_url, json=body)
        return json.loads(response.content)
    
    def modify_profile(data):
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
            if raw_field_name == 'state':
                current_value = current_value.upper()
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
                            TextBlock(text=current_value, isSubtle="true"),
                            "<",
                        Column()
            ])
            if pretty_name == 'Date of Birth':
                card.add(InputDate(ID=raw_field_name))
            elif pretty_name == "Sex":
                card.add(InputChoiceSet(ID="sex_choices", isMultiSelect="false", value=current_value))
                card.add(InputChoice(title="Male", value="1"))
                card.add(InputChoice(title="Female", value="2"))
                card.add(InputChoice(title="Custom", value="3"))
                card.add(InputChoice(title="Prefer Not to Say", value="4"))
                card.up_one_level()
                card.add(ActionSet())
                card.add(ActionShowCard(title="Custom Sex"), is_action=True)
                card.add(InputText(ID="custom_sex"))
            elif type(current_value) != str:
                card.add(InputNumber(ID=raw_field_name, placeholder=F"New {pretty_name}"))
            else:
                card.add(InputText(ID=raw_field_name, placeholder=f"New {pretty_name}"))

            # Return to main body again
            card.back_to_top()
            
        # Finish by adding global submit button
        card.add(Container(spacing="ExtraLarge", separator="true"))
        card.up_one_level()
        card.add(ActionSubmit(title="Submit All"), is_action=True)
        
        return card.to_json()
    
    # Retrieve account data from database
    db_response = query_database(f"SELECT * FROM [dbo].[Profile] WHERE account_id = '{account_id}'")
    data = db_response["ResultSets"]["Table1"][0]
    
    result = modify_profile(data)
    return func.HttpResponse(body=result, status_code=200)
