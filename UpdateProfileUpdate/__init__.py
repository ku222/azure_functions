import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests
import re
from datetime import datetime, timedelta

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve intent, data
    req_body = req.get_json()
    account_id = req_body.get('account_id')
    updates = req_body.get('updates')

    def query_database(query):
        logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
        body = {"intent": "query", "params": [query]}
        response = requests.post(url=logic_app_url, json=body)
        return json.loads(response.content)

    # Validation functions
    def validate_zipcode(zipcode_string):
        match = re.search(pattern=r'\d{5}', string=zipcode_string)
        if match:
            zipcode = match[0]
            if len(zipcode) == len(zipcode_string):
                return zipcode
        return False

    def validate_phonenumber(phone_number):
        numbers_only = re.sub(pattern=r'[^+0-9]', repl='', string=phone_number)
        if "+" in numbers_only:
            if len(numbers_only) > 12:
                return False
        else:
            if len(numbers_only) > 10:
                return False
        pattern = r'(\+1)?([2-9]{1}[0-9]{2})([2-9]{1}[0-9]{2})([0-9]{4})'
        matches = re.search(pattern, numbers_only)
        if matches:
            (country_digits, area_digits, exchange_digits, personal_digits) = matches.groups()
            return f"{area_digits}-{exchange_digits}-{personal_digits}"
        return False
    
    def validate_name(name_str):
        match = re.search(r'[a-zA-Z]+-?[a-zA-Z]*', name_str)
        if match:
            if len(match[0]) == len(name_str) and len(match[0]) > 1:
                return match[0]
        return False
    
    def validate_state(state):
        STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
        if state.upper() in STATES:
            return state.upper()
        return False
    
    def validate_email(email):
        if email.count("@") == 1 and email.count(".") >= 1:
            return True
        return False

    # Formatting Functions
    def format_dateofbirth(dob_string):
        (year, month, day) = dob_string.split('-')
        date = datetime.strptime(dob_string, "%Y-%m-%d")
        return {
            "fulldate": date.isoformat(),
            "age": (datetime.now() - date).days // 365,
            "day": day,
            "month": month,
            "year": int(year)
        }
        
    def update_profile(account_id, update_dict):
        update_query_list = []
        
        for (field_name, new_value) in update_dict.items():
            if new_value:
                ## Add date =============================================================
                if field_name == "fulldate":
                    date_dict = format_dateofbirth(new_value)
                    for (key, value) in date_dict.items():
                        if type(value) == str:
                            update_query_list.append(f"{key} = '{value}'")
                        else:
                            update_query_list.append(f"{key} = {value}")
                ## Add name fields =============================================================
                elif field_name in ('first', 'middle', 'last'):
                    valid = validate_name(new_value)
                    if valid:
                        update_query_list.append(f"{field_name} = '{new_value.title()}'")
                    else:
                        return "invalid name"
                ## Add phone number =============================================================
                elif field_name == "phone":
                    valid = validate_phonenumber(new_value)
                    if valid:
                        update_query_list.append(f"{field_name} = '{valid}'")
                    else:
                        return "invalid phone number"
                ## Add State =============================================================
                elif field_name == "state":
                    valid = validate_state(new_value)
                    if valid:
                        update_query_list.append(f"{field_name} = '{valid}'")
                    else:
                        return "invalid state"
                ## Add Zipcode =============================================================
                elif field_name == "zipcode":
                    valid = validate_zipcode(new_value)
                    if valid:
                        update_query_list.append(f"{field_name} = {valid}")
                    else:
                        return "invalid zipcode"
                ## Add Email =============================================================
                elif field_name == "email":
                    valid = validate_email(new_value)
                    if valid:
                        update_query_list.append(f"{field_name} = '{valid}'")
                    else:
                        return "invalid email address"
                ## All Others =============================================================
                else:
                    update_query_list.append(f"{field_name} = '{new_value}'")
                    
        if update_query_list:
            query = "UPDATE [dbo].[Profile] SET " + ', '.join(update_query_list) + f" WHERE account_id = '{account_id}'"
            # Make database update
            query_database(query)
            return "updated"
        return "not updated"
        
    # deserialize updates
    update_dict = json.loads(updates)
    result = update_profile(account_id=account_id, update_dict=update_dict)
    return func.HttpResponse(body=result, status_code=200)

