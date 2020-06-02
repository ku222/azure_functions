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
        then parses/formats the response from Azure maps nicely
        before handing it back to our bot
    
    Inputs:
        json request with an "address" Query parameter
        example:
        {"address": '<ADDRESS STRING>'}
        
    Outputs:
        HTTP 200 + nicely formatted address JSON if okay
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

    def parse_azuremaps_response(response, return_structured=True):
        '''Extract a nicely formatted address from the Azure maps response'''
        output = None
        point_addresses = [dict_ for dict_ in response.json()['results'] if dict_.get('type') == 'Point Address']
        if point_addresses:
            point_address = point_addresses[0].get('address')
            # Structure if we want
            if return_structured:
                output = {
                    'Format': 'structured',
                    'Street Number': point_address.get('streetNumber'),
                    'Street Name': point_address.get('streetName'),
                    'Town/City': point_address.get('municipality'),
                    'State': point_address.get('countrySubdivision'),
                    'Zip Code': point_address.get('postalCode')
                }
            # Else return unformatted
            else:
                output = {
                    'Format': 'unstructured',
                    'Address': point_address.get('freeformAddress')
                }
        return output
    
    # Call our functions above sequentially
    response = query_azure_maps(query)
    output = parse_azuremaps_response(response)
    
    # Check for output at all
    if not output:
        return func.HttpResponse(body='No Matching Address Found', status_code=400)
        
    # Convert our dict to a json serializable string
    output_json = json.dumps(output)
    # Add content-type = application/json to our headers
    output_headers = {'Content-Type': 'application/json'}
    # Return OK http response
    return func.HttpResponse(body=output_json, headers=output_headers, status_code=200)

