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
    data = req_body.get('data')
    language = req_body.get('language')

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
            "LoanOverpayment": "Show me my debts",
            "ManageProfile": "View my Profile",
            "NavigationBank": "Nearest banks to me",
            "BookAppointment": "Closest Lingfield branch to me",
            "ManageCards": "Reset my card pin number",
            "CreatePiggyBank": "Create a new piggy bank",
            "SmashPiggyBank": "Manage my piggy banks",
            "AddToPiggyBank": "Add to my piggy banks",
            "MonthlyAllowancePiggyBank": "Change my piggy bank monthly allowance",
            "MonthlySpendingBudget": "Put limits on my spending"
        }
        return dict_.get(dialog)
    
    def translate_list_of_strings(string_list, to_lang):
        base_url="https://api.cognitive.microsofttranslator.com/translate?api-version=3.0"
        translator_key="e8662f21ef0646a8abfab4f692e441ab"
        headers = {
                "Ocp-Apim-Subscription-Key": translator_key,
                "Content-Type": "application/json; charset=UTF-8",
                "Content-Length": str(len(string_list)),
                }
        # Construct body
        body = [{"Text": text} for text in string_list]
        # Post request, return
        response = requests.post(url=f"{base_url}&to={to_lang}", headers=headers, json=body)
        # Extract translations
        translated_output = []
        for response_dict in response.json():
                translations_array = response_dict['translations']
                first_result = translations_array[0]
                translated_text = first_result['text']
                translated_output.append(translated_text)
        return translated_output

    def get_recommended_prompts(data):
        recommender_url = "http://f91719c7-fa9b-4f2c-84b0-b5e8fc7d8302.uksouth.azurecontainer.io/score"
        response = requests.post(url=recommender_url, json={"data": data})
        recommended_dialogs = json.loads(json.loads(response.text)).get('result')
        recommended_prompts = [dialog_to_prompt(dialog) for dialog in recommended_dialogs]
        translated_prompts = translate_list_of_strings(recommended_prompts, to_lang=language)
        return translated_prompts
    
    recommended_prompts = get_recommended_prompts(data)
    result = json.dumps({"recommended_prompts": recommended_prompts})
    return func.HttpResponse(body=result, status_code=200)

