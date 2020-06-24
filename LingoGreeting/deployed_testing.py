
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

def get_firstname(account_id):
    db_dict = query_database("SELECT first FROM [dbo].[Profile]")
    return db_dict['ResultSets']['Table1'][0]['first'].title()

def dialog_to_prompt(dialog):
    dict_ = {
        "ViewTransactions": "View my last transactions",
        "SummariseTransactions": "Breakdown my spending",
        "MostExpensiveTransaction": "Most expensive transaction last week",
        "ReportTransactionFraud": "Report transaction as fraud",
        "MakeTransfer": "Give money to someone",
        "NewTransferee": "Add a new payee",
        "EditTransferee": "Add a new payee",
        "StandingOrder": "Create standing order",
        "ViewBalance": "How much money do I have",
        "ViewLoans": "Show me my loans",
        "LoanDetails": "Show me my mortgage",
        "LoanOverpayment": "Show me my loans",
        "ManageProfile": "View my Profile",
        "NavigationBank": "Nearest banks to me",
        "BookAppointment": "Closest Lingfield branch to me",
        "ManageCards": "Reset my card pin number",
        "CreatePiggyBank": "Create a new piggy bank",
        "SmashPiggyBank": "Manage my piggy banks",
        "AddToPiggyBank": "View my piggy banks",
        "MonthlyAllowancePiggyBank": "Manage my piggy banks",
        "MonthlySpendingBudget": "Put limits on my spending"
    }
    return dict_.get(dialog)
    
def create_welcome_card(account_id):
    firstname = get_firstname(account_id)
    # Create card
    blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
    bot_icon = "https://i.ibb.co/dmmWb6s/Lingo-Bot-Bare.png"

    card = AdaptiveCard(backgroundImage=blue_background)
    card.add([
        Container(),
            "<",
        Image(url=bot_icon, spacing="medium", height="130px", horizontalAlignment="center"),
        TextBlock(text=f"Welcome Back, {firstname}!", spacing="Large", weight="bolder", size="ExtraLarge", horizontalAlignment="center", color="light"),
        RichTextBlock(horizontalAlignment="center", spacing="Large"),
            TextRun(text="Im", wrap="true", size="medium", color="light"),
            TextRun(text=" Lingo ", weight="bolder", wrap="true", size="Large", color="light"),
            TextRun(text="your very own personal banking assistant.", wrap="true", size="medium", color="light"),
            "<",
        TextBlock(text="Here are some things you can ask me to help you with...", wrap="true", spacing="medium", horizontalAlignment="center", color="light" ),
    ])
    return card.to_json()
    

#%%

create_welcome_card(account_id)


#%%

url = "http://b5a8b487-b1e5-487a-8f1f-4c7fe94e470d.uksouth.azurecontainer.io/score"
response = requests.post(url=url, json={"account_id": "A00003088"})
json.loads(json.loads(response.text))
