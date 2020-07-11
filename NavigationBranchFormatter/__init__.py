import logging
import azure.functions as func
from math import sin, cos, sqrt, atan2, radians
import requests
import json
import io
from adaptivecardbuilder import *

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    ###############################################################
    ## Retrieve address
    ###############################################################
    req_body = req.get_json()
    address = req_body.get('address')
    language = req_body.get('language')
    
    ###############################################################
    ## Get lat+lon from address input using Azure Maps API
    ###############################################################
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
        return (float(lat), float(lon))
        
    def query_database(query):
        logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
        body = {"intent": "query", "params": [query]}
        response = requests.post(url=logic_app_url, json=body)
        return json.loads(response.content)
    
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
        db_dict = query_database("SELECT * FROM [dbo].[BranchWithGeo]")
        bank_rows = db_dict['ResultSets']['Table1']
        banks_list = []
        for row in bank_rows:
            # Create bank
            # Format Closing time
            splitted = row['Closes'].split(':')
            closing_time = splitted[0] + splitted[1]
            bank = Bank(name=row['AddressLine'], lat=row['Latitude'], lon=row['Longitude'],
                        opening_time=row['Opens'], closing_time=closing_time)
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
    def create_card(banks_list, language):
        # initialize our card
        card = AdaptiveCard()
        # loop over branches - each one will have a mini-card to itself
        for bank in banks_list:
            card.add(TextBlock(text=f"{bank.distance} miles away", separator="true", spacing="large"))
            card.add(ColumnSet())
            
            # First column - bank info
            card.add(Column(width=2))
            card.add(TextBlock(text="BANK OF LINGFIELD BRANCH"))
            card.add(TextBlock(text=bank.name, size="ExtraLarge", weight="Bolder", spacing="None", dont_translate=True))
            card.add(TextBlock(text=u"\u2605"*4+u"\u2606", spacing="None"))
            card.add(TextBlock(text=f"Opens at {str(bank.opening_time).zfill(4)}", isSubtle=True, spacing="None"))
            card.add(TextBlock(text=f"Closes at {str(bank.closing_time).zfill(4)}", isSubtle=True, spacing="None"))
            card.add(TextBlock(text="Matt H.: I'm compelled to give this place 5 stars due to the number of times I've chosen to bank here this past year!", size="Small", wrap="true"))
            
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
            card.add(ActionOpenUrl(url=f"https://cloudwars2composerdev.z22.web.core.windows.net/?lat={bank.lat}&lon={bank.lon}", title="View on Map", style="positive"), is_action=True)
            
            # create expandible card to show all our bank-specific appointment items
            card.add(ActionShowCard(title="View Open Appointment Slots", style="positive"), is_action=True)
            
            # Save a checkpoint at this level to come back to later
            action_showcard_level = card.save_level()

            # now loops over appointment items and add them
            for appointment in bank.appointments:
                card.add(ColumnSet(separator="true"))
                
                # Add our slots, start, end times
                row_items = [f"From: {appointment.start_time}", f"To: {appointment.end_time}"]
                for item in row_items:
                    card.add(Column(verticalContentAlignment="Center"))
                    card.add(TextBlock(text=item, horizontalAlignment="Center"))
                    card.up_one_level() # Back to column set level

                # Add the "Book This!" button, in the final column
                card.add(Column(verticalContentAlignment="Center"))
                card.add(ActionSet())
                book_button_data = {"branch_name": bank.name, "from_time": appointment.start_time, "to_time": appointment.end_time}
                card.add(ActionSubmit(title="Book!", style="positive", data=book_button_data), is_action=True)
                card.load_level(action_showcard_level) # back to showcard's body
            
            # Go back to the main body of the card, ready for next branch
            card.back_to_top()
            
        return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")
    
    ###############################################################
    ## MAIN
    ###############################################################
    # Call our functions above sequentially
    response = query_azure_maps(address)
    (lat, lon) = extract_coordinates(response)
    banks_list = get_closest_3_banks_list(lat1=lat, lon1=lon)
    card = create_card(banks_list, language)
    
    # Return OK http response
    return func.HttpResponse(body=card, status_code=200)

