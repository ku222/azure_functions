#%%
import logging
import azure.functions as func
import json
from adaptivecardbuilder import *

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    req_body = req.get_json()
    firstname = req_body.get('firstname')
    middlenames = req_body.get('middlenames')
    familyname = req_body.get('familyname')
    
    def create_card():
        card = AdaptiveCard(backgroundImage="https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png")
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
        
    result = create_card()
    return func.HttpResponse(body=result, status_code=200)
