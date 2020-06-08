import logging
import azure.functions as func
from math import sin, cos, sqrt, atan2, radians
import requests
import pandas as pd
import json
import io
from adaptivecardbuilder import *

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
            
        sorted_banks_list = sorted(banks_list, key=lambda bank: bank.distance, reverse=False)
        return sorted_banks_list[:3]
    
    ###############################################################
    ## Programmatically create adaptive card using our home-grown adaptivecardbuilder API
    ###############################################################
    def create_card(banks_list):
        # initialize our card
        card = AdaptiveCard()
        # loop over branches - each one will have a mini-card to itself
        for bank in banks_list:
            card.add(TextBlock(text=f"{bank.distance} miles away", separator="true", spacing="large"))
            card.add(ColumnSet())
            
            # First column - bank info
            card.add(Column(width=2))
            card.add(TextBlock(text="BANK OF LINGFIELD BRANCH"))
            card.add(TextBlock(text=bank.name, size="ExtraLarge", weight="Bolder", spacing="None"))
            card.add(TextBlock(text="5 stars", isSubtle=True, spacing="None"))
            card.add(TextBlock(text=f"Opens at {str(bank.opening_time).zfill(4)}", isSubtle=True, spacing="None"))
            card.add(TextBlock(text=f"Closes at {str(bank.closing_time).zfill(4)}", isSubtle=True, spacing="None"))
            card.add(TextBlock(text="**Matt H. said** Im compelled to give this place 5 stars due to the number of times Ive chosen to bank here this past year!", size="Small", wrap="true"))
            
            card.up_one_level() # Back up to column set
            
            # Second column - image
            card.add(Column(width=1))
            img = "https://s17026.pcdn.co/wp-content/uploads/sites/9/2018/08/Business-bank-account-e1534519443766.jpeg"
            card.add(Image(url=img))
            
            # Back to card's body container
            card.back_to_top()
        
            # add action set to contain our interactive elements
            card.add(ActionSet())

            # First add our "View on Map" button
            card.add(ActionOpenUrl(url=f"https://www.google.com/maps/@{bank.lat},{bank.lon},5.33z", title="View on Map"), is_action=True)
            
            # create expandible card to show all our bank-specific appointment items
            card.add(ActionShowCard(title="View Appointments"), is_action=True)
            
            # Save a checkpoint at this level to come back to later
            action_showcard_level = card.save_level()

            # now loops over appointment items and add them
            for appointment in bank.appointments:
                card.add(ColumnSet())
                
                # Add our slots, start, end times
                row_items = ["Slot", appointment.start_time, appointment.end_time]
                for item in row_items:
                    card.add(Column(style="emphasis", verticalContentAlignment="Center"))
                    card.add(TextBlock(text=item, horizontalAlignment="Center"))
                    card.up_one_level() # Back to column set level

                # Add the "Book This!" button, in the final column
                card.add(Column(style="emphasis", verticalContentAlignment="Center"))
                card.add(ActionSet())
                card.add(ActionSubmit(title="Book this!", data={"Appt": f"({appointment.start_time}, {appointment.end_time})"}), is_action=True)
                card.load_level(action_showcard_level) # back to showcard's body
            
            # Go back to the main body of the card, ready for next branch
            card.back_to_top()
            
        return card.to_json()
    
    ###############################################################
    ## MAIN
    ###############################################################
    (lat, lon) = get_lat_lon_from_address(address)
    banks_list = get_closest_3_banks_list(lat1=lat, lon1=lon)
    card = create_card(banks_list)
    
    # Return OK http response
    return func.HttpResponse(body=card, status_code=200)

