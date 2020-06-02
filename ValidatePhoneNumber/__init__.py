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

    # extract numbers via regex
    numbers_only = re.sub(pattern=r'[^+0-9]', repl='', string=number_str)

    # check for long numbers
    if len(numbers_only) > 12:
        return func.HttpResponse(body='Phone Number is Too Long', status_code=400)

    # extract US phone numbers of format +1 NXX-NXX-XXXX
    # Where N is 2-9 and X is 0-9
    pattern = r'(\+1)?([2-9]{1}[0-9]{2})([2-9]{1}[0-9]{2})([0-9]{4})'
    matches = re.search(pattern, numbers_only)

    if not matches:
        return func.HttpResponse(body='Invalid Phone Number', status_code=400)

    # unpack regex match groups
    (country_digits, area_digits, exchange_digits, personal_digits) = matches.groups()
    
    # add country code if not provided
    if not country_digits:
        country_digits = '+1'
    
    # format result before returning
    result = f"{country_digits} {area_digits}-{exchange_digits}-{personal_digits}"
    return func.HttpResponse(body=result, status_code=200)
