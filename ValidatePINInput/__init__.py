import logging
import azure.functions as func
import re

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve PIN
    PIN = req.params.get('PIN')
    
    if not PIN:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            PIN = req_body.get('PIN')
    
    if not PIN:
        return func.HttpResponse(body='PIN missing', status_code=400)
 
    numbers_only = re.sub(pattern=r'[^0-9]', repl='', string=PIN)
    
    if len(numbers_only) == 4:
        result = numbers_only
    else:
        result = "fail"
        
    return func.HttpResponse(body=result, status_code=200)