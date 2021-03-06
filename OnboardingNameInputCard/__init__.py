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
    language = req_body.get('language')
    
    def create_card(language):
        card = AdaptiveCard(backgroundImage="https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png")
        card.add([
            ColumnSet(),
                Column(width=2),
                    RichTextBlock(spacing="medium", separator="true"),
                        TextRun(text="First Name", color="light", weight="bolder"),
                        TextRun(text="*", color="attention", weight="bolder"),
                        "<",
                    InputText(ID="firstname", value=firstname if firstname else '', dont_translate=True),
                    
                    RichTextBlock(spacing="medium", separator="true"),
                        TextRun(text="Middle Names", color="light", weight="bolder"),
                        "<",
                    InputText(ID="middlenames", value=middlenames if middlenames else '', dont_translate=True),
                    
                    RichTextBlock(spacing="medium", separator="true"),
                        TextRun(text="Family Name", color="light", weight="bolder"),
                        TextRun(text="*", color="attention", weight="bolder"),
                        "<",
                    InputText(ID="familyname", value=familyname if familyname else '', dont_translate=True),
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

        return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")
        
    result = create_card(language)
    return func.HttpResponse(body=result, status_code=200)
