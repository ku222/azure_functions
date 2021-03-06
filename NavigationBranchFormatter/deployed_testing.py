
#%%

import requests

DEPLOYED_URL = 'http://cloudwars2functionapp.azurewebsites.net/api/NavigationBranchFormatter?code=GMtryo1P7lJD3Jq4K7ILowWbTC/HKfM97dZ6bNLqdV3e9xgISHCftw=='

json_payload = {'address': 'Beverly Hills, 90210'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)


#%%
from math import sin, cos, sqrt, atan2, radians
import json
import requests
from adaptivecardbuilder import *

address = "Beverly Hills, 90210"
language = "en"

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
    def format_times(self):
        self.start_time = self.start_time[:5]
        self.end_time = self.end_time[:5]
            
###############################################################
## Get closest 3 banks
###############################################################
def get_closest_3_banks_list(lat1, lon1):
    select_query = "SELECT Branch.Branch_ID, AddressLine, Latitude, Longitude, Opens, Closes, Appt.Start_Time, Appt.End_Time "
    from_query = "FROM [dbo].[BranchWithGeo] AS Branch LEFT JOIN [dbo].[BranchAppointments] AS Appt "
    on_query = "ON Branch.Branch_ID = Appt.Branch_ID"
    db_dict = query_database(select_query + from_query + on_query)
    bank_rows = db_dict['ResultSets']['Table1']
    bank_dict = dict()
    for row in bank_rows:
        branch_id = row['Branch_ID']
        if branch_id not in bank_dict:
            splitted = row['Closes'].split(':')
            closing_time = splitted[0] + splitted[1]
            bank = Bank(name=row['AddressLine'], lat=row['Latitude'], lon=row['Longitude'], opening_time=row['Opens'], closing_time=closing_time)
            bank_dict[branch_id] = bank
        else:
            bank = bank_dict[branch_id]
        # Add appointment
        appointment = Appointment(start_time=row['Start_Time'], end_time=row['End_Time'])
        appointment.format_times()
        bank.add_appointment(appointment)
        # get distance
        if not bank.distance:
            bank.set_distance(lat1=lat1, lon1=lon1)
    
    banks_list = list(bank_dict.values())
    sorted_banks_list = sorted(banks_list, key=lambda bank: bank.distance, reverse=False)
    return sorted_banks_list[:3]

###############################################################
## Programmatically create adaptive card using our home-grown adaptivecardbuilder API
###############################################################
def create_card(banks_list, language):
    
    def to_datetime(hrs_mins):
        return datetime.datetime.strptime(hrs_mins, '%H:%M')
    
    # Utility time functions
    def get_hrs_mins():
        now = datetime.datetime.now()
        hrs_mins = f"{now.hour}:{now.minute}"
        return to_datetime(hrs_mins)
    
    hrs_mins_now = get_hrs_mins()
    
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
        card.add(TextBlock(text="Matt H.: Im compelled to give this place 5 stars due to the number of times Ive chosen to bank here this past year!", size="Small", wrap="true"))
        
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
        card.add(ActionShowCard(title="View Appointment Slots", style="positive"), is_action=True)
        
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
            if to_datetime(appointment.start_time) > hrs_mins_now:
                card.add(ActionSet())
                book_button_data = {"branch_name": bank.name, "from_time": appointment.start_time, "to_time": appointment.end_time}
                card.add(ActionSubmit(title="Book!", style="positive", data=book_button_data), is_action=True)
            else:
                card.add(TextBlock(text="Already Over", isSubtle="true", horizontalAlignment="center"))
            card.load_level(action_showcard_level) # back to showcard's body
        
        # Go back to the main body of the card, ready for next branch
        card.back_to_top()
        
    if language == 'en':
        return card.to_json()
    return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")

###############################################################
## MAIN
###############################################################
# Call our functions above sequentially
response = query_azure_maps(address)
(lat, lon) = extract_coordinates(response)
banks_list = get_closest_3_banks_list(lat1=lat, lon1=lon)
card = create_card(banks_list, language)

#%%

card