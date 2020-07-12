import logging
import azure.functions as func
from math import sin, cos, sqrt, atan2, radians
import requests
import json
import io
from adaptivecardbuilder import *
import datetime

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    ###############################################################
    ## Retrieve address
    ###############################################################
    req_body = req.get_json()
    branch_name = req_body.get('branch_name')
    language = req_body.get('language')
    
    def query_database(query):
        logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
        body = {"intent": "query", "params": [query]}
        response = requests.post(url=logic_app_url, json=body)
        return json.loads(response.content)

    # Create lite class to help with parsing
    class Bank:
        def __init__(self, name, lat, lon, opening_time, closing_time):
            self.name = name
            self.lat = lat
            self.lon = lon
            self.opening_time = opening_time
            self.closing_time = closing_time
            self.appointments = []
            
        def add_appointment(self, appointment):
            self.appointments.append(appointment)

        def similarity(self, str2):
            str1 = self.name
            m = len(str1)
            n = len(str2)
            lensum = float(m + n)
            d = []           
            for i in range(m+1):
                d.append([i])        
            del d[0][0]    
            for j in range(n+1):
                d[0].append(j)       
            for j in range(1,n+1):
                for i in range(1,m+1):
                    if str1[i-1] == str2[j-1]:
                        d[i].insert(j,d[i-1][j-1])           
                    else:
                        minimum = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+2)         
                        d[i].insert(j, minimum)
            ldist = d[-1][-1]
            ratio = (lensum - ldist)/lensum
            return ratio
        
    class Appointment:
        def __init__(self, start_time, end_time):
            self.start_time = start_time
            self.end_time = end_time
        def format_times(self):
            self.start_time = self.start_time[:5]
            self.end_time = self.end_time[:5]
                

    def get_closest_3_banks_list(query_string):
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
        
        banks_list = list(bank_dict.values())
        sorted_by_similarity = sorted(banks_list, key=lambda bank: bank.similarity(query_string), reverse=True)
        return sorted_by_similarity[:3]


    def create_card(banks_list, language):
        
        # Utility time functions
        def to_datetime(hrs_mins):
            return datetime.datetime.strptime(hrs_mins, '%H:%M')
        def get_hrs_mins():
            now = datetime.datetime.now()
            hrs_mins = f"{now.hour}:{now.minute}"
            return to_datetime(hrs_mins)
        hrs_mins_now = get_hrs_mins()
        
        # initialize our card
        card = AdaptiveCard()
        # loop over branches - each one will have a mini-card to itself
        for bank in banks_list:
            card.add(ColumnSet(separator="true", spacing="large"))
            
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

    banks_list = get_closest_3_banks_list(query_string=branch_name)
    card = create_card(banks_list=banks_list, language=language)
    
    # Return OK http response
    return func.HttpResponse(body=card, status_code=200)

