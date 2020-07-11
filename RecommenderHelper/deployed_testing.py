
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
data = account_id
language = "ms"

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

#%%

from collections import defaultdict

def query_database(query):
    logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
    body = {"intent": "query", "params": [query]}
    response = requests.post(url=logic_app_url, json=body)
    return json.loads(response.content)

def get_email_addresses(account_id_array):
    stringified = ', '.join([f"'{ID}'" for ID in account_id_array])
    query = f"SELECT account_id, email, LanguagePreference FROM [dbo].[Profile] WHERE account_id IN ({stringified})"
    db_dict = query_database(query)
    output = defaultdict(list)
    for row in db_dict['ResultSets']['Table1']:
        output[row.get('account_id')].append((row['email'], row['LanguagePreference']))
    return output


#%%
account_id_array = ['A00003088']
get_email_addresses(account_id_array)


