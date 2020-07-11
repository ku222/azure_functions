import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve account number
    req_body = req.get_json()            
    account_id = req_body.get('account_id')
    from_time = req_body.get('from_time')
    to_time = req_body.get('to_time')
    branch_name = req_body.get('branch_name')
    language = req_body.get('language')

    def query_database(query):
        logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
        body = {"intent": "query", "params": [query]}
        response = requests.post(url=logic_app_url, json=body)
        return json.loads(response.content)

    def create_appointment_form(data, from_time, to_time, branch_name, language):
        # Dict mapping database names to pretty names
        DB_TO_CARD = {
        'first': 'First Name',
        'middle': 'Middle Name',
        'last': 'Last Name',
        'phone': 'Phone Number',
        'email': 'Email Address'
        }
        
        # Remove any unneeded keys
        profile_dict = {k:v for (k,v) in data.items() if k in DB_TO_CARD}
        
        # Rearrange keys so name ones are first, then all others after
        name_keys = ("first", "middle", "last")
        names_dict = {k:v for (k,v) in profile_dict.items() if k in name_keys}
        non_names_dict = {k:v for (k,v) in profile_dict.items() if k not in name_keys}
        names_dict.update(non_names_dict)
        profile_dict = names_dict
        
        # Initialize card
        card = AdaptiveCard(backgroundImage="https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png")

        # Add Title Container
        card.add(Container(backgroundImage="https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg"))
        card.add(TextBlock(text=f"Appointment Booking at", wrap="true", weight="bolder", size="Large", horizontalAlignment="center"))
        card.add(TextBlock(text=branch_name, wrap="true", weight="bolder", size="Large", horizontalAlignment="center", dont_translate=True))
        card.up_one_level()
        
        # Add From + To container
        card.add(Container(backgroundImage="https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg"))
        card.add([
            ColumnSet(),
                Column(),
                    RichTextBlock(horizontalAlignment="center"),
                        TextRun(text="From: "),
                        TextRun(text=from_time, size="medium", weight="bolder", dont_translate=True),
                        "<",
                    "<",
                Column(),
                    RichTextBlock(horizontalAlignment="center"),
                        TextRun(text="To: "),
                        TextRun(text=to_time, size="medium", weight="bolder", dont_translate=True),
                        "<",
                    "<",
                "<",
        ])
        card.back_to_top()
        
        # Fill in Personal Details Form
        card.add(Container(backgroundImage="https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg"))
        container_level = card.save_level()
        for (raw_field_name, current_value) in profile_dict.items():
            # prettify name
            pretty_name = DB_TO_CARD.get(raw_field_name)
            current_value = current_value.title()            
            # add to card
            card.add([
                "items-------",
                ColumnSet(spacing="medium", separator="true"),
                    Column(width=1, verticalContentAlignment="center"),
                        TextBlock(text=pretty_name, weight="Bolder"),
                        "<",
                    Column(width=2, verticalContentAlignment="center"),
                        InputText(ID=pretty_name, value=current_value, dont_translate=True),
            ])
            card.load_level(container_level)
        
        # Add Reason for Booking
        reasons = ["Loan Enquiries", "Balance Enquiries", "Opening a New Account", "Gush about Lingo"]
        card.add([
            ColumnSet(spacing="medium", separator="true"),
                Column(width=1, verticalContentAlignment="center"),
                    TextBlock(text="Reason for Visit", weight="Bolder"),
                    "<",
                Column(width=2, verticalContentAlignment="center"),
                    InputChoiceSet(ID="reason", style="compact"),
                    [InputChoice(title=reason, value=f"{i}") for (i, reason) in enumerate(reasons)]
        ])
        
        # Finish by adding update action button
        card.back_to_top()
        card.add(ActionSubmit(title="Book Appointment!", style="positive", data={"action": "book"}), is_action=True)
        card.add(ActionSubmit(title="Cancel", style="destructive", data={"action": "cancel"}), is_action=True)
        return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")
    
    # Retrieve account data from database
    db_response = query_database(f"SELECT * FROM [dbo].[Profile] WHERE account_id = '{account_id}'")
    data = db_response["ResultSets"]["Table1"][0]

    # Create card
    result = create_appointment_form(data=data, from_time=from_time, to_time=to_time, branch_name=branch_name, language=language)
    return func.HttpResponse(body=result, status_code=200)

