
#%%

import requests

DEPLOYED_URL = 'http://cloudwars2functionapp.azurewebsites.net/api/ValidateAddress?code=BA77aXBrSHU0L7hb4FQkvxfoK/VHVYfAEdbEwqCNoBcbwYOWRzQOog=='
json_payload = {'address': '15127 NE 24th Street, Redmond, WA'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)



# %%
from adaptivecardbuilder import *

firstname = 'hiel'
middlenames = 'dd'
familyname= 'ff'

def create_card():
    card = AdaptiveCard(backgroundImage="https://lh3.googleusercontent.com/proxy/1OKoCOxXegrIjs7o4lM5pXe60d-cuRvdxb9skqw3Fw6G7-TYokRImgR_bh-fj1_SsWkYzxIlHD0hxEs1dRa5dfAhyvb3jSI0LCKJ_UeCxH0YTOzn12sU_YuL3g8")
    card.add([
        ColumnSet(),
            Column(width=2),
                RichTextBlock(spacing="medium", separator="true"),
                    TextRun(text="First Name", color="light", weight="bolder"),
                    TextRun(text="*", color="attention", weight="bolder"),
                    "<",
                InputText(ID="firstname", value=firstname if firstname else ''),
                
                RichTextBlock(spacing="medium", separator="true"),
                    TextRun(text="Middle Names", color="light", weight="bolder"),
                    "<",
                InputText(ID="middlenames", value=middlenames if middlenames else ''),
                
                RichTextBlock(spacing="medium", separator="true"),
                    TextRun(text="Family Name", color="light", weight="bolder"),
                    TextRun(text="*", color="attention", weight="bolder"),
                    "<",
                InputText(ID="familyname", value=familyname if familyname else ''),
                "<",
                
            Column(width=1),
                "<",
            "<",
        
        RichTextBlock(separator="true", spacing="Large"),
            TextRun(text="*", color="attention", weight="bolder"),
            TextRun(text="Required", color="light", weight="bolder"),
            "<",
            
        ActionSet(spacing="small"),
            "action",
            ActionSubmit(title="Go!", style="positive")
    ])

    return card.to_json()

create_card()
