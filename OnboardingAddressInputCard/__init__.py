#%%
import logging
import azure.functions as func
import json
from adaptivecardbuilder import *

def main(req: func.HttpRequest) -> func.HttpResponse:

    # Try retrieve address dictionary from input
    req_body = req.get_json()
    address_line1 = req_body.get('address_line1')
    address_line2 = req_body.get('address_line2')
    city = req_body.get('city')
    state = req_body.get('state')
    zipcode = req_body.get('zipcode')

    def create_card():
        # Params
        fields = (address_line1, address_line2, city, state, zipcode)
        field_names = ('Street Address Line 1', 'Street Address Line 2', 'City', 'State', 'Zip Code')
        ID_names = ('address_line1', 'address_line2', 'city', 'state', 'zipcode')
        placeholders = ('101 First Ave.', '', 'Elkridge', 'TX', '12340')
        requireds = (True, False, True, True, True)

        # Construct card
        card = AdaptiveCard(backgroundImage="https://lh3.googleusercontent.com/proxy/1OKoCOxXegrIjs7o4lM5pXe60d-cuRvdxb9skqw3Fw6G7-TYokRImgR_bh-fj1_SsWkYzxIlHD0hxEs1dRa5dfAhyvb3jSI0LCKJ_UeCxH0YTOzn12sU_YuL3g8")
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

        # Add other empty column to make everything left-aligned
        card.up_one_level()
        card.add(Column(width=1))

        # Add required reminder
        card.back_to_top()
        card.add(RichTextBlock(separator="true", spacing="Large"))
        card.add(TextRun(text="*", color="attention", weight="bolder"))
        card.add(TextRun(text="Required", color="light", weight="bolder"))
        
        # Add global submit action
        card.up_one_level()
        card.add(ActionSet(spacing="small"))
        card.add(ActionSubmit(title="Submit!", style="positive"), is_action=True)
        
        return card.to_json()
        
    result = create_card()
    return func.HttpResponse(body=result, status_code=200)