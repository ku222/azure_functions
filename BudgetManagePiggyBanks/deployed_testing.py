
#%%

import requests
import json

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/ViewProfile?code=pa7gOnUTxIPwEeN13gHpeN4gqgkg9agdZZh/XTjC2ABquysNfZDYLQ=='
json_payload = {"account_id": 'A00000001'}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%% Example payload in dict form
# u'\u2588'

from adaptivecardbuilder import *
import requests
import json

account_id = 'A00003088'

def query_database(query):
    logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
    body = {"intent": "query", "params": [query]}
    response = requests.post(url=logic_app_url, json=body)
    return json.loads(response.content)

# Retrieve account balance
db_dict = query_database(f"SELECT * from [dbo].[Piggybank] WHERE account_id = '{account_id}'")
piggybank_list = db_dict["ResultSets"]["Table1"]

piggybank_list


#%% Creation Page

from adaptivecardbuilder import *
import requests
import json


blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
piggy_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Piggy_Bank_or_Savings_Flat_Icon_Vector.svg/1024px-Piggy_Bank_or_Savings_Flat_Icon_Vector.svg.png"


def create_piggybanks(piggybank_list):
    card = AdaptiveCard()
    for piggy_dict in piggybank_list:
        piggybank_name = piggy_dict["piggybank_name"]
        amount = piggy_dict["amount"]
        created_date = piggy_dict["created_date"].split('T')[0]
        monthly_allowance = piggy_dict["monthly_allowance"]
        # add to card
        card.add(Container(backgroundImage=blue_background))
        card.add(TextBlock(text=piggybank_name, color="light", size="Large", weight="Bolder", horizontalAlignment="center"))
        card.add(TextBlock(text=f"Amount: ${amount:,}", color="light", size="medium", horizontalAlignment="center"))
        card.add(TextBlock(text=f"Born: {created_date}", color="light", size="medium", horizontalAlignment="center"))
        if monthly_allowance > 0:
            card.add(TextBlock(text=f"Monthly allowance: ${monthly_allowance:,}", color="light", size="medium", horizontalAlignment="center"))
        card.add(Image(url=piggy_icon, height="170px", horizontalAlignment="center"))
        card.add(ActionSet(separator="true", spacing="medium"))
        card.add(ActionSubmit(title="Add to Piggy Bank", style="positive", data={"action": "add", "piggybank_name": piggybank_name}), is_action=True)
        card.add(ActionSubmit(title="Change Monthly Allowance", style="positive", data={"action": "change_allowance", "piggybank_name": piggybank_name}), is_action=True)
        card.add(ActionSubmit(title="Smash Piggy Bank", style="destructive", data={"action": "smash", "piggybank_name": piggybank_name}), is_action=True)
        card.back_to_top()        
    
    return card.to_json()
        
create_piggybanks(piggybank_list)


#%% Adding Money Page

coin_icon = "https://i.ibb.co/7pSTx1L/coin.png"
card = AdaptiveCard(backgroundImage=blue_background)

current_balance = 1324.44

card.add([
    TextBlock(text="Add to your Piggy Bank", color="light", size="Large", weight="Bolder", horizontalAlignment="center"),
    RichTextBlock(horizontalAlignment="center"),
        TextRun(text="Account balance: ", color="light", size="medium"),
        TextRun(text=f"${current_balance:,}", color="light", weight="bolder", size="medium"),
        "<",
    ColumnSet(),
        Column(),
            Container(spacing="small"), "<",
            Container(spacing="medium"), "<",
            Image(url=coin_icon, height="100px", horizontalAlignment="center"),
            "<",
        Column(),
            Image(url=piggy_icon, height="140px", horizontalAlignment="center"),
            "<",
        "<",
    
    TextBlock(text="Type in an amount to add", horizontalAlignment="center", color="light"),
    ColumnSet(),
        Column(width=1),
            TextBlock(text="$", color="light", size="Large", verticalAlignment="center", horizontalAlignment="right"),
            "<",
        Column(width=5),
            InputNumber(ID="amount", placeholder="50.00"),
            ActionSet(separator="true", spacing="medium"),
                "action",
                ActionSubmit(title="Add Funds!", style="positive"),
                "<",
            "<",
        "items",
        Column(width=1),
            "<",
        "<"
])

card.to_json()


#%% Card Creation

piggy_text1 = "Lingfield Piggy Banks are a great way to set money aside, away from your main balance." 
piggy_text2 = "You could try putting the money you need for bills into a pot as soon as you get paid, and only moving it back into your account when you need it."
piggy_text3 = "This means you can set aside everything you need to spend on bills, rent or mortgage payments safely, so you do not spend it accidentally!" 
piggy_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Piggy_Bank_or_Savings_Flat_Icon_Vector.svg/1024px-Piggy_Bank_or_Savings_Flat_Icon_Vector.svg.png"

trainer_text1 = "Enlist your very own personal financial trainer to get your budgeting into shape!"
trainer_text2 = "Set monthly spending budgets for each category of spending, helping you reach your saving goals."
trainer_text3 = "As you spend, we will let you know how close you are getting to your spending limit for each category." 
trainer_text4 = "We will not stop you from spending over these limits - but it is a gentle reminder to stay on track."

blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
white_background = "https://www.publicdomainpictures.net/pictures/30000/velka/plain-white-background.jpg"



card = AdaptiveCard()
card.add([
    "items",
    Container(backgroundImage=blue_background),
        TextBlock(text="Lingfield Piggy banks".title(), color="light", size="ExtraLarge", weight="Bolder", spacing="ExtraLarge", horizontalAlignment="center"),
        Image(url=piggy_icon, height="170px", horizontalAlignment="center"),
        TextBlock(text=f"Set money aside for bills, fees, or a rainy day", wrap="true", color="light", horizontalAlignment="center", size="medium", separator="true"),
        Container(spacing="small"),
            "<",
        ActionSet(),
            "action",
            ActionShowCard(title="Learn More"),
                "item",
                Container(backgroundImage=white_background),
                    "item",
                    TextBlock(text=piggy_text1, wrap="true"),
                    TextBlock(text=piggy_text2, wrap="true"),
                    TextBlock(text=piggy_text3, wrap="true"),
                    ActionSet(),
                        "action",
                        ActionSubmit(title="Create a new Piggy Bank", data={"action": "piggy"}),
                        "<",
                    "<",
                "<",
            "<",
        "items",
        Container(spacing="Small"),
            "<",
        "<",
        
        
    "items",
    Container(spacing="Small"),
        "<",
    Container(backgroundImage=blue_background),
        TextBlock(text="Personal (Financial) Trainer".title(), color="light", size="ExtraLarge", weight="Bolder", spacing="ExtraLarge", horizontalAlignment="center"),
        Container(spacing="Large"),
            "<",
        Image(url="https://i.ibb.co/vH4BM82/referee.png", height="120px", horizontalAlignment="center"),
        Container(spacing="Large"),
            "<",
        TextBlock(text=f"Get tough on your budgeting with monthly goals", wrap="true", color="light", horizontalAlignment="center", size="medium", separator="true"),
        ActionSet(),
            "action",
            ActionShowCard(title="Learn More"),
                "item",
                Container(backgroundImage=white_background),
                    "item",
                    TextBlock(text=trainer_text1, wrap="true"),
                    TextBlock(text=trainer_text2, wrap="true"),
                    TextBlock(text=trainer_text3, wrap="true"),
                    TextBlock(text=trainer_text4, wrap="true"),
                    ActionSet(),
                        "action",
                        ActionSubmit(title="Create a new Piggy Bank", data={"action": "piggy"}),
                        "<",
                    "<",
                "<",
            "<",
        "items",
        Container(spacing="Small")
])

card.to_json()


#%%


{
    "schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.2",
    "type": "AdaptiveCard",
    "body": [
        {
            "type": "TextBlock",
            "text": "Add to your Piggy Bank",
            "color": "light",
            "size": "Large",
            "weight": "Bolder",
            "horizontalAlignment": "center"
        },
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "items": [
                        {
                            "type": "Container",
                            "items": [],
                            "spacing": "small"
                        },
                        {
                            "type": "Container",
                            "items": [],
                            "spacing": "medium"
                        },
                        {
                            "type": "Image",
                            "url": "https://i.ibb.co/7pSTx1L/coin.png",
                            "height": "100px",
                            "horizontalAlignment": "center"
                        }
                    ]
                },
                {
                    "type": "Column",
                    "items": [
                        {
                            "type": "Image",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Piggy_Bank_or_Savings_Flat_Icon_Vector.svg/1024px-Piggy_Bank_or_Savings_Flat_Icon_Vector.svg.png",
                            "height": "140px",
                            "horizontalAlignment": "center"
                        }
                    ]
                },
                {
                    "type": "TextBlock",
                    "text": "Add funds into your new Piggy Bank",
                    "color": "light"
                },
                {
                    "type": "Input.Number",
                    "id": "amount",
                    "placeholder": "50.00"
                }
            ]
        }
    ],
    "actions": [],
    "backgroundImage": "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
}