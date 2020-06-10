
#%%

import requests
import json

intent = "display"
data = "{\r\n  \"OutputParameters\": {},\r\n  \"ResultSets\": {\r\n    \"Table1\": [\r\n      {\r\n        \"card_id\": \"V00000001\",\r\n        \"disp_id\": \"D00000009\",\r\n        \"type\": \"VISA Infinite\",\r\n        \"year\": 2018,\r\n        \"month\": \"10\",\r\n        \"day\": \"16\",\r\n        \"fulldate\": \"2018-10-16T00:00:00\",\r\n        \"Pin_Code\": 7650,\r\n        \"Status\": \"Inactive\"\r\n      },\r\n      {\r\n        \"card_id\": \"V00000002\",\r\n        \"disp_id\": \"D00000019\",\r\n        \"type\": \"VISA Signature\",\r\n        \"year\": 2018,\r\n        \"month\": \"3\",\r\n        \"day\": \"13\",\r\n        \"fulldate\": \"2018-03-13T00:00:00\",\r\n        \"Pin_Code\": 7916,\r\n        \"Status\": \"Lost/Stolen\"\r\n      },\r\n      {\r\n        \"card_id\": \"V00000003\",\r\n        \"disp_id\": \"D00000041\",\r\n        \"type\": \"VISA Infinite\",\r\n        \"year\": 2015,\r\n        \"month\": \"9\",\r\n        \"day\": \"3\",\r\n        \"fulldate\": \"2015-09-03T00:00:00\",\r\n        \"Pin_Code\": 3467,\r\n        \"Status\": \"Active\"\r\n      }\r\n    ]\r\n  }\r\n}"
DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/ManageCards?code=yvmb8yIHQMQfzHhqa9/THqgkM5xauddovKZdL0VrhLIpsVx/HXzhuw=='
json_payload = {'intent': intent, 'data': data}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%% Example payload in dict form

data = {
"OutputParameters": {},
"ResultSets": {
"Table1": [
  {
    "card_id": "V00000001",
    "disp_id": "D00000009",
    "type": "VISA Infinite",
    "year": 2018,
    "month": "10",
    "day": "16",
    "fulldate": "2018-10-16T00:00:00",
    "Pin_Code": 7650,
    "Status": "Frozen"
  },
  {
    "card_id": "V00000002",
    "disp_id": "D00000019",
    "type": "VISA Signature",
    "year": 2018,
    "month": "3",
    "day": "13",
    "fulldate": "2018-03-13T00:00:00",
    "Pin_Code": 7916,
    "Status": "Lost/Stolen"
  },
  {
    "card_id": "V00000003",
    "disp_id": "D00000041",
    "type": "VISA Infinite",
    "year": 2015,
    "month": "9",
    "day": "3",
    "fulldate": "2015-09-03T00:00:00",
    "Pin_Code": 3467,
    "Status": "Active"
  }
]
}
}


#%%

import json
from adaptivecardbuilder import *

data = "{\r\n  \"OutputParameters\": {},\r\n  \"ResultSets\": {\r\n    \"Table1\": [\r\n      {\r\n        \"card_id\": \"V00000001\",\r\n        \"disp_id\": \"D00000009\",\r\n        \"type\": \"VISA Infinite\",\r\n        \"year\": 2018,\r\n        \"month\": \"10\",\r\n        \"day\": \"16\",\r\n        \"fulldate\": \"2018-10-16T00:00:00\",\r\n        \"Pin_Code\": 7650,\r\n        \"Status\": \"Frozen\"\r\n      },\r\n      {\r\n        \"card_id\": \"V00000002\",\r\n        \"disp_id\": \"D00000019\",\r\n        \"type\": \"VISA Signature\",\r\n        \"year\": 2018,\r\n        \"month\": \"3\",\r\n        \"day\": \"13\",\r\n        \"fulldate\": \"2018-03-13T00:00:00\",\r\n        \"Pin_Code\": 7916,\r\n        \"Status\": \"Lost/Stolen\"\r\n      },\r\n      {\r\n        \"card_id\": \"V00000003\",\r\n        \"disp_id\": \"D00000041\",\r\n        \"type\": \"VISA Infinite\",\r\n        \"year\": 2015,\r\n        \"month\": \"9\",\r\n        \"day\": \"3\",\r\n        \"fulldate\": \"2015-09-03T00:00:00\",\r\n        \"Pin_Code\": 3467,\r\n        \"Status\": \"Active\"\r\n      }\r\n    ]\r\n  }\r\n}"
data = json.loads(data)
    # Serialize our data into a python dict
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
        "^"
        ])
        
    return adaptive.to_json()

display_cards(data)
#%%

{
    "schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.2",
    "type": "AdaptiveCard",
    "body": [
        {
            "type": "Image",
            "url": "https://brokerchooser.com/uploads/images/digital-banks/n26-review-bank-card.png"
        }
    ],
    "actions": [],
    "backgroundImage": "https://i.dlpng.com/static/png/6774669_preview.png"
}