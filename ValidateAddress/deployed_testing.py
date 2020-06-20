
#%%

import requests

json_payload = {
        "address_line1": "15127 NE 24th Street",
        "address_line2": "",
        "city": "Redmond",
        "state": "WA",
        "zipcode": "85326"
    }

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/ValidateAddress?code=BA77aXBrSHU0L7hb4FQkvxfoK/VHVYfAEdbEwqCNoBcbwYOWRzQOog=='
response = requests.post(url=DEPLOYED_URL, json=json_payload)

response.text

# %%

import re
import json
import requests
from adaptivecardbuilder import *
import azure.functions as func

address = "{\r\n  \"address_line1\": \"15127 NE 24th Street\",\r\n  \"address_line2\": \"\",\r\n  \"city\": \"Redmond\",\r\n  \"state\": \"WA\",\r\n  \"zipcode\": \"85326\"\r\n}"
address_dict = json.loads(address)

def main(address_dict):

    def fully_validate_input(address_dict):
        # Validate that we have any input at all
        def is_empty(address_dict):
            m1 = '' if address_dict['address_line1'] else "First address line"
            m2 = '' if address_dict['state'] else "State"
            m3 = '' if address_dict['city'] else "City"
            m4 = '' if address_dict['zipcode'] else "Zip Code"
            error_messages = [message for message in (m1, m2, m3, m4) if message]
            if error_messages:
                beginning = 'please fill in the '
                middle = ', '.join(error_messages) if len(error_messages) != 2 else ' and '.join(error_messages)
                end = " fields." if len(error_messages) > 1 else " field."
                return beginning + middle + end
            return False
    
        def is_valid_state(address_dict):
            state = address_dict['state']
            STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
                "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
                "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
                "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
                "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
            if state.upper() in STATES:
                return True
            return False
    
        def is_valid_zipcode(address_dict):
            zipcode_string = address_dict['zipcode']
            match = re.search(pattern=r'\d{5}', string=zipcode_string)
            if match:
                zipcode = match[0]
                if len(zipcode) == len(zipcode_string):
                    return True
            return False
        
        # Run all validation functions in sequence
        if is_empty(address_dict):
            errors = is_empty(address_dict)
            return func.HttpResponse(body=errors, status_code=400)

        if not is_valid_state(address_dict):
            return func.HttpResponse(body="the state you entered is not a valid US state.", status_code=400)
    
        if not is_valid_zipcode(address_dict):
            return func.HttpResponse(body="the zip code you entered is not a valid US zip code", status_code=400)

    def query_azure_maps(_query_):
        '''Send query to azure maps service with parameters below'''
        _format_ = 'json'
        _subscription_key_ = 'd5vwJomzaZQjWo1BCYXsNyMOm1QHAxZ9Ie-MkszAzrw'
        _country_set_ = 'US'
        url = f"https://atlas.microsoft.com/search/address/{_format_}?subscription-key={_subscription_key_}&countrySet={_country_set_}&api-version=1.0&query={_query_}"
        response = requests.get(url=url)
        return response

    def parse_azuremaps_response(response):
        '''Extract a nicely formatted address from the Azure maps response'''
        def address_result_to_dict(address_result):
            address = address_result.get('address')
            return {'Street Number': address.get('streetNumber'),
                    'Street Name': address.get('streetName'),
                    'Town/City': address.get('municipality'),
                    'State': address.get('countrySubdivision'),
                    'Zip Code': address.get('postalCode'),
                    'Free Form': address.get('freeformAddress')}
        
        all_address_results = [dict_ for dict_ in response.json()['results']]
        point_addresses = [dict_ for dict_ in response.json()['results'] if dict_.get('type') == 'Point Address']
        if point_addresses:
            return [address_result_to_dict(address_result) for address_result in point_addresses]
        return [address_result_to_dict(address_result) for address_result in all_address_results]
    
    def create_address_selection_card(array_of_address_dicts):
        card = AdaptiveCard(backgroundImage="https://wallpaperplay.com/walls/full/5/9/5/37696.jpg")
        card.add(Container(backgroundImage="https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg"))
        container_level = card.save_level()
        valid_counter = 0
        for address_dict in array_of_address_dicts:
            if address_dict['Street Number'] != None:
                valid_counter += 1
                card.add([
                    "items---",
                    ColumnSet(separator="true", spacing="medium"),
                        Column(width=2, verticalContentAlignment="center"),
                            TextBlock(text=address_dict['Free Form'], wrap="true"),
                            "<",
                        Column(width=1, verticalContentAlignment="center"),
                            ActionSet(),
                                "action---",
                                ActionSubmit(title="Correct", style="positive", data=address_dict),
                ])
                card.load_level(container_level)
        
        if valid_counter == 0:
            return func.HttpResponse(body="no potentially matching addresses were found", status_code=400)
        return card.to_json()

    ### Call our functions above sequentially
    fully_validate_input(address_dict)
    address_query = ' '.join(address_dict.values())
    response = query_azure_maps(address_query)
    array_of_address_dicts = parse_azuremaps_response(response)
    result = create_address_selection_card(array_of_address_dicts)
    return result

result = main(address_dict)

# %%

result