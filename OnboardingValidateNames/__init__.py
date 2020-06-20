import logging
import azure.functions as func
import re
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    firstname = req_body.get('firstname')
    middlenames = req_body.get('middlenames')
    familyname = req_body.get('familyname')
    
    if not firstname:
        return func.HttpResponse(body="you must enter a first name", status_code=400)

    if not familyname:
        func.HttpResponse(body="you must enter a family name", status_code=400)
    
    def validate_and_clean_name(name_str):
        valid = True
        # Search for any non-legal chars
        valid = False if re.search(pattern=r"[^a-zA-Z'\s-]", string=name_str) else valid
        # Search for any consecutive non letters
        valid = False if re.search(pattern=r"[^a-zA-Z]{2}", string=name_str) else valid
        # Now clean up
        if valid:
            splitted = name_str.split(' ')
            titled = [word.title() for word in splitted]
            joined = ' '.join(titled)
            return joined
        return valid
    
    clean_firstname = validate_and_clean_name(firstname)
    clean_middlenames = validate_and_clean_name(middlenames)
    clean_familyname = validate_and_clean_name(familyname)
    
    if not clean_firstname or not clean_familyname:
        return func.HttpResponse(body="names can only contain letters, apostrophes, or dashes, and cannot have consecutive non-letter characters.", status_code=400)
    
    if middlenames:
        if not clean_middlenames:
            return func.HttpResponse(body="names can only contain letters, apostrophes, or dashes, and cannot have consecutive non-letter characters.", status_code=400)
    
    result = json.dumps({
        "firstname": clean_firstname,
        "middlenames": clean_middlenames,
        "familyname": clean_familyname
    })
    headers = {'Content-Type': 'application/json'}
    return func.HttpResponse(body=result, headers=headers, status_code=200)