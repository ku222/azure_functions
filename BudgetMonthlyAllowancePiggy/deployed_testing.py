
#%%

import requests
import json

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/BudgetMonthlyAllowancePiggy?code=LvJ6nbVoR3V09C4LazQWhOEI2xjqyqeablfjrE/a08GTpQ/WlbfqzA=='
json_payload = {"account_id": 'A00003088', "piggybank_name": "Mortgage"}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%% Example payload in dict form
# u'\u2588'

from adaptivecardbuilder import *
import requests
import json


account_id = "A00003088"
piggybank_name = "Holiday2"
language = 'ms'

def query_database(query):
    logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
    body = {"intent": "query", "params": [query]}
    response = requests.post(url=logic_app_url, json=body)
    return json.loads(response.content)

# Retrieve account balance
db_dict = query_database(f"SELECT balance from [dbo].[Profile] WHERE account_id = '{account_id}'")
balance = db_dict['ResultSets']['Table1'][0]['balance']

# Retrieve current monthly allowance for the current piggybank
db_dict = query_database(f"SELECT monthly_allowance from [dbo].[PiggyBank] WHERE account_id = '{account_id}' AND piggybank_name = '{piggybank_name}'")
monthly_allowance = db_dict['ResultSets']['Table1'][0]['monthly_allowance']

def create_addfunds_card(balance, piggybank_name, monthly_allowance, language):
    blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
    piggy_icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Piggy_Bank_or_Savings_Flat_Icon_Vector.svg/1024px-Piggy_Bank_or_Savings_Flat_Icon_Vector.svg.png"
    coin_icon = "https://i.ibb.co/7pSTx1L/coin.png"
    
    # Initialize card
    card = AdaptiveCard(backgroundImage=blue_background)

    # Add card elements
    card.add([
        RichTextBlock(horizontalAlignment="center"),
            TextRun(text=piggybank_name, color="light", size="Large", weight="Bolder", horizontalAlignment="center", dont_translate=True),
            TextRun(text="Piggy Bank", color="light", size="Large", weight="Bolder", horizontalAlignment="center"),
            "<",
        TextBlock(text=f"Account Balance: ${balance:,}", color="light", weight="bolder", size="medium", horizontalAlignment="center"),
        TextBlock(text=f"Current Monthly Allowance: ${monthly_allowance:,}", color="light", weight="bolder", size="medium", horizontalAlignment="center"),
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
        
        TextBlock(text="Set new monthly allowance", horizontalAlignment="center", color="light"),
        ColumnSet(),
            Column(width=1),
                TextBlock(text="$", color="light", size="Large", verticalAlignment="center", horizontalAlignment="right"),
                "<",
            Column(width=5),
                InputNumber(ID="amount", placeholder="50.00", dont_translate=True),
                ActionSet(separator="true", spacing="medium"),
                    "action",
                    ActionSubmit(title="Set New Allowance!", style="positive"),
                    ActionSubmit(title="Cancel", style="destructive", data={"action": "cancel"}),
                    "<",
                "<",
            "items",
            Column(width=1),
                "<",
            "<"
    ])
    # Serialize to json
    return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")

# Create card
result = create_addfunds_card(balance, piggybank_name, monthly_allowance, language)


#%%

result