import logging
import azure.functions as func
import re

def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Purpose:
        Given a user-inputted, 4-digit PIN, checks strength
    
    Inputs:
        json request with a "PIN" Query parameter
        example:
        {"PIN": '<4-digit PIN>'}
        
    Outputs:
        HTTP 200 and PIN strength rating
        HTTP 400 otherwise
    '''
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve number string
    PIN = req.params.get('PIN')
    
    # general error handler - taken from example documentation
    if not PIN:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            PIN = req_body.get('PIN')
    
    # final check that we have some value
    if not PIN:
        return func.HttpResponse(body='No PIN Provided', status_code=400)
    
    # PIN strength function
    def rate_my_PIN(PIN):
        # pure ascending/descending numbers check
        asc = desc = True
        rep_count = consec_count = 0
        for i in range(len(PIN)-1):
            asc = asc and (PIN[i] < PIN[i+1]) # check if all ascending
            desc = desc and (PIN[i] > PIN[i+1]) # check all descending
            rep_count += (PIN[i] == PIN[i+1]) # count neighbor repetitions
            consec_count += abs(int(PIN[i]) - int(PIN[i+1])) == 1 # count neighbor consecutives
        
        penalty_count = (asc*4 + desc*4 + consec_count**2 + rep_count**2)
        print(penalty_count)
        if penalty_count <= 1:
            rating = 'Very Strong'
        elif penalty_count <= 3:
            rating = 'Strong'
        elif penalty_count < 5:
            rating = 'Medium Strength'
        else:
            rating = 'Weak'
        return rating
            
    rating = rate_my_PIN(PIN)
    return func.HttpResponse(body=rating, status_code=200)