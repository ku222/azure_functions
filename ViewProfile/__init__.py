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
            
    if not account_id:
        return func.HttpResponse(body='Account ID missing', status_code=400)
    
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
        card = AdaptiveCard(backgroundImage="https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png")
        card.add(Container(backgroundImage="https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg"))
        container_level = card.save_level()
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
                            "<",
                        Column(),
                            TextBlock(text=current_value, isSubtle="true", wrap="true"),
            ])
            card.load_level(container_level)
        
        # Finish by adding update action button
        card.back_to_top()
        card.add(Container(spacing="medium", separator="true"))
        card.up_one_level()
        card.add(ActionSubmit(title="Update Profile", style="positive", data={"action": "update"}), is_action=True)
        
        return card.to_json()

    # Retrieve account data from database
    db_response = query_database(f"SELECT * FROM [dbo].[Profile] WHERE account_id = '{account_id}'")
    data = db_response["ResultSets"]["Table1"][0]

    # Create card
    result = display_profile(data)

    return func.HttpResponse(body=result, status_code=200)

