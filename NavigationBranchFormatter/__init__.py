import logging
import azure.functions as func
from math import sin, cos, sqrt, atan2, radians
import requests
import pandas as pd
import json
import io

def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    Purpose:
        Given an address,
        will get distances to all nearby banks
        then return the top 3 banks, distances to them,
        opening hours, and free appointment slots,
        all in an adaptive card
    
    Inputs:
        json request with this schema:
            {"coordinates": "4.314,-44.8865"}
        
    Outputs:
        HTTP 200 and interactive adaptive card
        HTTP 400 otherwise
    '''
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    ###############################################################
    ## Retrieve address
    ###############################################################
    address = req.params.get('address')
    
    # general error handler - taken from example documentation
    if not address:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            address = req_body.get('address')
    
    # final check that we have some value
    if not address:
        return func.HttpResponse(body='No Address Provided', status_code=400)

    ###############################################################
    ## Get lat+lon from address input using Azure Maps API
    ###############################################################
    def get_lat_lon_from_address(address):
        ## Let's call our already-deployed GetLatLonFromAnAddress function app
        DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/GetLatLonFromAnAddress?code=ucwQTFn4ivV/uycR72H3o7EIoSC28cDHynS8jFmlZ8Zwuy2iuL4yaQ=='
        json_payload = {'address': address}
        response = requests.post(url=DEPLOYED_URL, json=json_payload)
        coordinates = response.text
        (lat, lon) = coordinates.split(',')
        (lat, lon) = float(lat), float(lon)
        return (lat, lon)
    
    ###############################################################
    ## Create bank and appointment classes to help us with data parsing
    ###############################################################
    class Bank:
        def __init__(self, name, lat, lon, opening_time, closing_time):
            self.name = name
            self.lat = lat
            self.lon = lon
            self.distance = None
            self.opening_time = opening_time
            self.closing_time = closing_time
            self.appointments = []
            
        def add_appointment(self, appointment):
            self.appointments.append(appointment)
        
        def set_distance(self, lat1, lon1):
            R = 6373.0 # approximate radius of earth in km
            lat1 = radians(lat1)
            lon1 = radians(lon1)
            lat2 = radians(self.lat)
            lon2 = radians(self.lon)
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            self.distance = round(distance*0.621371, 2) # convert to miles
                
    class Appointment:
        def __init__(self, start_time, end_time):
            self.start_time = start_time
            self.end_time = end_time
                
    ###############################################################
    ## Get closest 3 banks
    ###############################################################
    def get_closest_3_banks_list(lat1, lon1):
        url = 'https://raw.githubusercontent.com/ku222/azure_functions/master/NavigationBranchFormatter/branch.txt' 
        urlData = requests.get(url).content
        df = pd.read_csv(io.StringIO(urlData.decode('utf-8')), sep='\t')
        banks_list = []
        for (i, row) in df.iterrows():
            # Create bank
            bank = Bank(name=row['AddressLine'], lat=row['Latitude'], lon=row['Longitude'],
                        opening_time=row['Opens'], closing_time=row['Closes'])
            # Create appointments
            appointment1 = Appointment(start_time="09:00", end_time="10:00")
            appointment2 = Appointment(start_time="10:30", end_time="11:00")
            # Add appointments
            bank.add_appointment(appointment1)
            bank.add_appointment(appointment2)
            # get distance
            bank.set_distance(lat1=lat1, lon1=lon1)
            # Add to list
            banks_list.append(bank)
            
        sorted_banks_list = sorted(banks_list, key=lambda bank: bank.distance, reverse=True)
        return sorted_banks_list[:3]
    
    ###############################################################
    ## Programmatically create our adaptive card
    ###############################################################
    def create_card(banks_list):
        # Initialize Card schema
        card = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.0",
            "body": [
                {
                    "type": "Container",
                    "items": []
                }
            ]
        }
        
        card_items = card['body'][0]['items']
        
        # Add items
        for (i, bank) in enumerate(banks_list):
            all_elements = []
            # Header + Separator
            header = {
                "type": "TextBlock",
                "text": f"{bank.distance} miles away",
                "spacing": "large",
                "separator": "True"
            }
            # Initialize the columns set
            column_set = {
                "type": "ColumnSet",
                "columns": []
            }
            
            # Now for 2-width column
            for _ in range(1):
                column_width_2 = {
                    "type": "Column",
                    "width": 2,
                    "items": []
                }
                # Add elements to 2-width column
                for _ in range(1): 
                    # Add title to the 2-width column
                    column_width_2['items'].append({
                        "type": "TextBlock",
                        "text": "BANK OF LINGFIELD BRANCH"
                    })
                    # Add name of the branch in bold
                    column_width_2['items'].append({
                        "type": "TextBlock",
                        "text": f"{bank.name}",
                        "weight": "Bolder",
                        "size": "ExtraLarge",
                        "spacing": "None"
                    })
                    # Add rating
                    column_width_2['items'].append({
                        "type": "TextBlock",
                        "text": "4.2 Stars",
                        "isSubtle": "True",
                        "spacing": "None"
                    })
                    # Add review
                    column_width_2['items'].append({
                        "type": "TextBlock",
                        "text": "**Matt H. said** Im compelled to give this place 5 stars due to the number of times Ive chosen to bank here this past year!",
                        "size": "Small",
                        "wrap": "True"
                    })
                    
            # Now for the 1-width column
            for _ in range(1):
                column_width_1 = {
                    "type": "Column",
                    "width": 1,
                    "items": []
                }
                # Add image to the column
                for _ in range(1):
                    column_width_1['items'].append({
                        "type": "Image",
                        "url": "https://s17026.pcdn.co/wp-content/uploads/sites/9/2018/08/Business-bank-account-e1534519443766.jpeg",
                        "size": "auto",
                        "altText": "Seated guest drinking a cup of coffee"
                        })
                    
            # Add 2-width and 1-width columns to the column set (2 -> 1)
            column_set['columns'].append(column_width_2)
            column_set['columns'].append(column_width_1)
            
            # Add header and column set to all container
            all_elements.append(header)
            all_elements.append(column_set)
            
            #################################################################
            # Now for actions
            action_set = {
                "type": "ActionSet",
                "actions": []
            }
            
            # Add show me on a map button to actions set
            show_me_on_map_button = {
                "type": "Action.OpenUrl",
                "title": "Show me on a map!",
                "url": "https://adaptivecards.io"
            }
            
            # action set has an expandible "show card"
            showcard = {
                "type": "Action.ShowCard",
                "title": "Show Available Appointments",
                "card": {
                    "type": "AdaptiveCard",
                    "body": []
                }
            }

            # add actions to the show card's body - one per appointment
            showcard_body = showcard['card']['body']
            
            for (j, appointment) in enumerate(bank.appointments):
                showcard_column_set = {
                    "type": "ColumnSet",
                    "style": "emphasis",
                    "columns": []
                }
                
                showcard_column_set_columns = showcard_column_set['columns']
                # Add Appointment margin
                showcard_column_set_columns.append({
                    "type": "Column",
                    "style": "emphasis",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": f"Appointment {j+1}"
                        }
                    ],
                    "bleed": "true",
                    "width": "auto"
                })
                
                # Add start time label
                showcard_column_set_columns.append({
                    "type": "Column",
                    "style": "emphasis",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": f"{appointment.start_time}"
                        }
                    ],
                    "width": "auto"
                })
                
                # Add end time label
                showcard_column_set_columns.append({
                    "type": "Column",
                    "style": "emphasis",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": f"{appointment.end_time}"
                        }
                    ],
                    "width": "auto"
                })
                
                # Add appointment booking button
                showcard_column_set_columns.append({
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {
                            "type": "ActionSet",
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": "Book This!"
                                }
                            ]
                        }
                    ]
                })
                
                # Add column set to showcard body
                showcard_body.append(showcard_column_set)
                
            # Add the above actions to the action set
            action_set['actions'].append(showcard)
            action_set['actions'].append(show_me_on_map_button)
            
            # Add to all elements
            all_elements.append(action_set)
            card_items.extend(all_elements)
            
        return card

    ###############################################################
    ## MAIN
    ###############################################################
    (lat, lon) = get_lat_lon_from_address(address)
    banks_list = get_closest_3_banks_list(lat1=lat, lon1=lon)
    card = create_card(banks_list)
    
    # Return OK http response
    return func.HttpResponse(body=json.dumps(card), status_code=200)

