import logging
import re
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Purpose:
        Given a user-inputted phone number, checks that it is a 
        valid US phone number (+1 NXX-NXX-XXXX)
    
    Inputs:
        json request with a "number" Query parameter
        example:
        {"number": '<NUMBER STRING>'}
        
    Outputs:
        HTTP 200 + nicely formatted number if okay
        HTTP 400 + error message otherwise
    '''
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve number string
    number_str = req.params.get('number')
    
    # general error handler - taken from example documentation
    if not number_str:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            number_str = req_body.get('number')
    
    # final check that we have some value
    if not number_str:
        return func.HttpResponse(body='No Number Provided', status_code=400)

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
    
    result = validate_phonenumber(number_str)
    if not result:
        func.HttpResponse(body="that phone number was not of the correct format", status_code=400)
        
    return func.HttpResponse(body=result, status_code=200)
