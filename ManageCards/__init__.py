import logging
import azure.functions as func
import json
from adaptivecardbuilder import *

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve intent, data
    intent = req.params.get('intent')
    data = req.params.get('data')
    
    # general error handler - taken from example documentation
    if not intent:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            intent = req_body.get('intent')
       
    if not data:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            data = req_body.get('data')
            
    if not intent:
        return func.HttpResponse(body='Intent missing', status_code=400)
    
    if not data:
        return func.HttpResponse(body='Data missing', status_code=400)
    
    # Serialize our data into a python dict
    data = json.loads(data)
    
    # Make up some dummy transaction data
    headers = ['ID', 'Amount', 'Receiver', 'Date', 'Suspicious']
    table = [['TRN-349824', '$400.50', 'Walmart', '29-05-2020'],
            ['TRN-334244', '$50.35', 'Delta Airlines', '01-06-2020'],
            ['TRN-503134', '$60.50', 'Smoothie King', '03-06-2020']]
    
    def display_cards(data):
        adaptive = AdaptiveCard()
        cards = data["ResultSets"]["Table1"]

        for card in cards:
            font_color = "default"
            backgroundImage_url = "https://i.dlpng.com/static/png/6774669_preview.png" if card["Status"]=="Frozen" else ""
            
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
                                ActionSubmit(title="Reset PIN", data={"card": f"{card['card_id']}", "action": "PIN"}, style="positive"),
                                ActionSubmit(title="Defrost Card" if card["Status"]=="Frozen" else "Freeze Card",
                                            data={
                                                "card": f"{card['card_id']}",
                                                "action": f"{'unfreeze' if card['Status']=='Frozen' else 'freeze'}"
                                                }
                                            ,
                                            style="positive"),
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
            
            # Go back up to main body
            adaptive.back_to_top()
            
        return adaptive.to_json()
    
    result = display_cards(data)
    return func.HttpResponse(body=result, status_code=200)