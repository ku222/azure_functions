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
    language = req_body.get('language')
   
    dialogs_dict = {
        "Help": ["Help", "Please Help"],
        "Sign up with us": ["Join the Bank of Lingfield", "Sign up with you"],
        "Change Language": ["Speak in Russian", "Translate to French"],
        "Search Bing": ["Search the Internet", "Google something please"],
        "Login": ["Login", "I want to Login"],
        "Manage your Profile": ["View my profile", "Update my address"],
        "Book an Appointment": ["Book an Appointment", "Book a face to face"],
        "Manage your Cards": ["Change my PIN", "Manage my Cards"],
        "Transfer Funds": ["Give money to someone", "Send money to frank"],
        "Add a transferee": ["Add a new transferee", "Add a new payee"],
        "Summarise your Transactions": ["How am I spending money", "Split out my spending"],
        "See Most Expensive Transaction": ["Most expensive transaction last week", "Most costly transaction"],
        "Report a Fradulent Transaction": ["Money has been taken from my account", "Report a fraud"],
        "Set up a Standing Order": ["Create standing order", "Set up recurring transaction"],
        "Manage your Mortgages and Loans": ["Show me my mortgage", "Show me my debts"],
        "View your Balance": ["Show me my balance", "How much money do I have?"],
        "Find nearby Branches": ["Find nearby banks", "Find a Bank of Lingfield Branch"],
        "View Budgeting Options": ["Help with Budgeting", "Help curb my spending"],
        "Create a Pot of Money for Saving": ["Create a new Piggy Bank", "Create a new pot of money"],
        "Manage your Pots of Money": ["Smash a Piggy Bank", "Pay myself an allowance"],
        "Set Budgeting Targets": ["Put limits on my spending", "Set a monthly budget"]
    }

    def display_dialogs(dialogs_dict, language):
        blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
        card = AdaptiveCard(backgroundImage=blue_background)
        for (dialog, example_phrases) in dialogs_dict.items():
            (phrase1, phrase2) = example_phrases
            card.add([
                "items",
                ActionSet(),
                    "action",
                    ActionShowCard(title=dialog),
                        "items",
                        TextBlock(text=f'Type: "{phrase1}"', horizontalAlignment="center"),
                        TextBlock(text=f'Type: "{phrase2}"', horizontalAlignment="center", separator="true"),
            "^"
            ])

        if language == 'en':
            return card.to_json()
        return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")

    # Create card
    result = display_dialogs(dialogs_dict, language)
    return func.HttpResponse(body=result, status_code=200)

