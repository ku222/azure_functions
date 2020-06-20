
#%%

import requests

DEPLOYED_URL = 'http://cloudwars2functionapp.azurewebsites.net/api/ValidateAddress?code=BA77aXBrSHU0L7hb4FQkvxfoK/VHVYfAEdbEwqCNoBcbwYOWRzQOog=='
json_payload = {'address': '15127 NE 24th Street, Redmond, WA'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)



# %%
from adaptivecardbuilder import *

address_line1 = ""
address_line2 = ""
city = "New York"
state = "NY"
zipcode = ""

# Params
fields = (address_line1, address_line2, city, state, zipcode)
field_names = ('Street Address Line 1', 'Street Address Line 2', 'City', 'State', 'Zip Code')
ID_names = ('address_line1', 'address_line2', 'city', 'state', 'zipcode')
placeholders = ('101 First Ave.', '', 'Elkridge', 'TX', '12340')
requireds = (True, False, True, True, True)

card = AdaptiveCard(backgroundImage="https://wallpaperplay.com/walls/full/5/9/5/37696.jpg")
card.add(ColumnSet())
card.add(Column(width=2))
for (field, field_name, ID, placeholder, required) in zip(fields, field_names, ID_names, placeholders, requireds):
    card.add(RichTextBlock(separator="true", spacing="medium"))
    card.add(TextRun(text=field_name, color="light", weight="bolder"))
    if required:
        card.add(TextRun(text="*", color="attention", weight="bolder"))
    card.up_one_level()
    if field: # if field has value passed
        card.add(InputText(ID=ID, value=field))
    else:
        card.add(InputText(ID=ID, placeholder=placeholder))

card.up_one_level()
card.add(Column(width=1))

card.back_to_top()
card.add(RichTextBlock(separator="true", spacing="Large"))
card.add(TextRun(text="*", color="attention", weight="bolder"))
card.add(TextRun(text="Required", color="light", weight="bolder"))
card.up_one_level()
card.add(ActionSet(spacing="small"))
card.add(ActionSubmit(title="Submit!", style="positive"), is_action=True)
card.to_json()
