
#%%

import requests
import json

prompt = "Type a 4-digit pin below"
placeholder = "Type here"
submit_title = "Reset my PIN"

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/InputCard?code=8PxznKG3yJ02hoLcqUliERBqDqXq4M231LOvy9Je9qh73kqWunJx6w=='
json_payload = {'prompt': prompt, 'placeholder': placeholder, 'submit_title': submit_title}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%% Example payload in dict form



prompt = "Type a 4-digit pin below"
placeholder = "Type here"
submit_title = "Reset my PIN"

card = AdaptiveCard()
card.add([
    "items",
    TextBlock(text=prompt, weight="Bolder", separator="true"),
    InputText(ID="input", placeholder=placeholder),
    
    "Actions",
    ActionSubmit(title=submit_title)
])
card.to_json()


#%%
    # Serialize our data into a python dict
    
import json
from adaptivecardbuilder import *

data = "{\r\n  \"OutputParameters\": {},\r\n  \"ResultSets\": {\r\n    \"Table1\": [\r\n      {\r\n        \"card_id\": \"V00000001\",\r\n        \"disp_id\": \"D00000009\",\r\n        \"type\": \"VISA Infinite\",\r\n        \"year\": 2018,\r\n        \"month\": \"10\",\r\n        \"day\": \"16\",\r\n        \"fulldate\": \"2018-10-16T00:00:00\",\r\n        \"Pin_Code\": 7650,\r\n        \"Status\": \"Inactive\"\r\n      },\r\n      {\r\n        \"card_id\": \"V00000002\",\r\n        \"disp_id\": \"D00000019\",\r\n        \"type\": \"VISA Signature\",\r\n        \"year\": 2018,\r\n        \"month\": \"3\",\r\n        \"day\": \"13\",\r\n        \"fulldate\": \"2018-03-13T00:00:00\",\r\n        \"Pin_Code\": 7916,\r\n        \"Status\": \"Lost/Stolen\"\r\n      },\r\n      {\r\n        \"card_id\": \"V00000003\",\r\n        \"disp_id\": \"D00000041\",\r\n        \"type\": \"VISA Infinite\",\r\n        \"year\": 2015,\r\n        \"month\": \"9\",\r\n        \"day\": \"3\",\r\n        \"fulldate\": \"2015-09-03T00:00:00\",\r\n        \"Pin_Code\": 3467,\r\n        \"Status\": \"Active\"\r\n      }\r\n    ]\r\n  }\r\n}"

headers = ['ID', 'Amount', 'Receiver', 'Date', 'Suspicious']
table = [['TRN-349824', '$400.50', 'Walmart', '29-05-2020'],
        ['TRN-334244', '$50.35', 'Delta Airlines', '01-06-2020'],
        ['TRN-503134', '$60.50', 'Smoothie King', '03-06-2020']]
    
data = json.loads(data)

#%%

def display_cards(data):
    adaptive = AdaptiveCard()
    cards = data["ResultSets"]["Table1"]

    for card in cards:
        font_color = "default"
        backgroundImage_url = "https://i.dlpng.com/static/png/6774669_preview.png" if card["Status"]=="Frozen" else "https://www.publicdomainpictures.net/pictures/30000/velka/plain-white-background.jpg"
        
        adaptive.add([
            "items----",
            Container(backgroundImage=backgroundImage_url, spacing="large", separator="true"),
                ColumnSet(),
                    Column(),
                        TextBlock(text=card["card_id"], color=font_color),
                        TextBlock(text=card["type"], size="ExtraLarge", weight="Bolder", color=font_color),
                        TextBlock(text=f"Status: {card['Status']}", size="medium", weight="Bolder", color=font_color),
                        TextBlock(text=f"Expires {card['month']}-{card['day']}-{card['year']}", color=font_color),
                        TextBlock(text=f"PIN: {card['Pin_Code']}", color=font_color),
                        "<",
                    Column(),
                        Image(url="https://brokerchooser.com/uploads/images/digital-banks/n26-review-bank-card.png"),
                        "<",
                    "<",
                    
                    ActionSet(),
                        "actions ----",
                        ActionShowCard(title="Manage Card"),
                            ActionSubmit(title="Reset PIN", data={"card": f"{card['card_id']}", "action": "PIN"}),
                            ActionSubmit(title="Defrost Card" if card["Status"]=="Frozen" else "Freeze Card",
                                        data={
                                            "card": f"{card['card_id']}",
                                            "action": f"{'unfreeze' if card['Status']=='Frozen' else 'freeze'}"
                                            }
                                        ),
                                        "<",
                        ActionShowCard(title="View Transactions"),
                            "items ----"
        ])
        
        # Now to add transactions
        adaptive.add(ColumnSet())
        for header in headers:
            adaptive.add([
                Column(),
                    TextBlock(text=header, horizontalAlignment="center", weight="Bolder"),
                    "<"
            ])
        
        # up from columnset back to showcard body
        adaptive.up_one_level()
        # create saved pointer level
        showcard_body_level = adaptive.save_level()
        
        # Add transactions
        for transaction in table:
            adaptive.add(ColumnSet())
            
            # Add elements
            for element in transaction:
                adaptive.add([
                    Column(),
                        TextBlock(text=element, horizontalAlignment="center"),
                        "<"
                ])
            
            # Before moving to the next row, add a "Flag" button
            adaptive.add(Column())
            adaptive.add(ActionSet())
            flag_url = "https://pngimage.net/wp-content/uploads/2018/06/red-flag-png-5.png"
            transaction_id = transaction[0]
            submit_data = {"ID": transaction_id} # data to submit to our hosting interface
            adaptive.add(ActionSubmit(iconUrl=flag_url, data=submit_data), is_action=True)
            adaptive.load_level(showcard_body_level) # Go back to the top level, ready to add our next row
        
        adaptive.back_to_top()
        
    return adaptive.to_json()

display_cards(data)

#%%

from adaptivecardbuilder import *

card = AdaptiveCard()

image = "https://i.ytimg.com/vi/tsjd7xdgfjA/maxresdefault.jpg"
text = "Welcome to your Galaxy"
icon = "https://www.brandeps.com/icon-download/P/Planet-icon-vector-01.svg"
description = "Where the sky is not the limit and the service is out of this world"
transactions = ["earth", "mars", "venus", "jupiter"]

card.add([
    "items",
    Container(backgroundImage=image),
        TextBlock(text=text, color="light", horizontalAlignment="center"),
        TextBlock(text=description, color="light", horizontalAlignment="center", spacing="ExtraLarge"),
        ColumnSet()
])

for i in range(5):
    card.add(Column())
    card.add(Image(url=icon))
    card.up_one_level()

card.to_json()


#%%
