import logging
import azure.functions as func
from math import sin, cos, sqrt, atan2, radians
import requests
import pandas as pd
from card_constructor import create_card

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
        DEPLOYED_URL = 'http://cloudwars2functionapp.azurewebsites.net/api/ValidatePINStrength?code=SsjG8i3VjwFGEJyZKuEh5g/rHzu3thZWO4bFUiPTB19HM0iNIGFogQ=='
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
            self.distance = distance
                
    class Appointment:
        def __init__(self, start_time, end_time):
            self.start_time = start_time
            self.end_time = end_time
                
    ###############################################################
    ## Get closest 3 banks
    ###############################################################
    def get_closest_3_banks_list(lat1, lon1):
        df = pd.read_csv('branch.csv')
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
            banks_list.append(banks_list)
            
        sorted_banks_list = sorted(banks_list, key=lambda bank: bank.distance, reverse=True)
        return sorted_banks_list[:3]
    
    ###############################################################
    ## MAIN
    ###############################################################
    (lat, lon) = get_lat_lon_from_address(address)
    banks_list = get_closest_3_banks_list(lat1=lat, lon1=lon)
    card = create_card(banks_list)
    
    # Return OK http response
    return func.HttpResponse(body=card, status_code=200)