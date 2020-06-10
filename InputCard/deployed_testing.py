
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

import json
from adaptivecardbuilder import *
import re

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
            "type": "Container",
            "items": [
                {
                    "type": "TextBlock",
                    "text": "Type a 4-digit pin below",
                    "weight": "Bolder",
                    "separator": "true"
                },
                {
                    "type": "Input.Text",
                    "id": "input",
                    "placeholder": "Type here"
                }
            ],
            "style": "emphasis",
            "bleed": "true"
        },
        {
            "type": "Action.Submit",
            "title": "Reset my PIN"
        }
    ],
    "actions": []
}