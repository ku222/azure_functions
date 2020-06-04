#%%
import logging
import azure.functions as func

import re
import requests
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Purpose:
        Given a free-form address, passes it to Azure Maps
        then returns lat and lon
    
    Inputs:
        json request with an "address" Query parameter
        example:
        {"address": '<ADDRESS STRING>'}
        
    Outputs:
        HTTP 200 + latlon if OK
        HTTP 400 + error message otherwise
    '''
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve address string
    query = req.params.get('address')
    
    # general error handler - taken from example documentation
    if not query:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            query = req_body.get('address')
    
    # final check that we have some value
    if not query:
        return func.HttpResponse(body='Could Not Retrieve Address from Input', status_code=400)

    def query_azure_maps(_query_):
        '''Send query to azure maps service with parameters below'''
        _format_ = 'json'
        _subscription_key_ = 'd5vwJomzaZQjWo1BCYXsNyMOm1QHAxZ9Ie-MkszAzrw'
        _country_set_ = 'US'
        url = f"https://atlas.microsoft.com/search/address/{_format_}?subscription-key={_subscription_key_}&countrySet={_country_set_}&api-version=1.0&query={_query_}"
        response = requests.get(url=url)
        return response

    def extract_coordinates(response):
        '''Extract the best lat+lon match from the Azure maps response'''
        locations = [dict_ for dict_ in response.json()['results']]
        if locations:
            closest = locations[0]
            position = closest.get('position')
            (lat, lon) = position.get('lat'), position.get('lon')
        return (lat, lon)
    
    # Call our functions above sequentially
    response = query_azure_maps(query)
    (lat, lon) = extract_coordinates(response)
    
    output = f"{lat},{lon}"
    
    # Return OK http response
    return func.HttpResponse(body=output, status_code=200)

