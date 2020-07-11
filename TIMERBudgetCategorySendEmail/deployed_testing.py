
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
from datetime import date
import random
from collections import defaultdict

def query_database(query):
    logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
    body = {"intent": "query", "params": [query]}
    response = requests.post(url=logic_app_url, json=body)
    return json.loads(response.content)

def get_account_id_array():
    db_dict = query_database(f"SELECT account_no FROM [dbo].[Account]")
    return [dict_.get('account_no') for dict_ in db_dict['ResultSets']['Table1']]

def get_category_budget_dict():
    db_dict = query_database(f"SELECT * FROM [dbo].[CategoryBudget]")
    output = defaultdict(dict)
    for row_dict in db_dict['ResultSets']['Table1']:
        account_id = row_dict.get('account_id')
        category = row_dict.get('category')
        budget = row_dict.get('budget')
        output[account_id][category] = budget
    return output

def get_this_month_category_spending(account_id):
    query = f'''
    SELECT transaction_category, SUM(WITHDRAWAL_AMT) AS spending FROM [dbo].[Transaction_with_category] 
    WHERE MONTH(date) = MONTH(CURRENT_TIMESTAMP) AND YEAR(date) = YEAR(CURRENT_TIMESTAMP) AND account_no = '{account_id}'
    GROUP BY transaction_category
    '''
    db_dict = query_database(query.replace('\n', ' '))
    output = dict()
    rows = db_dict['ResultSets']['Table1']
    for row_dict in rows:
        category = row_dict.get('transaction_category')
        spending = row_dict.get('spending')
        output[category] = spending
    return output

def get_email_dict(account_id_array, category_budget_dict):
    email_dict = defaultdict(dict)
    for account_id in account_id_array:
        if account_id in category_budget_dict:
            this_month_spending_dict = get_this_month_category_spending(account_id)
            account_budget_dict = category_budget_dict.get(account_id)
            for (category, spending) in this_month_spending_dict.items():
                category = category.title()
                category_budget = account_budget_dict.get(category)
                if category_budget != None:
                    if spending >= 0.8*category_budget:
                        email_dict[account_id][category] = (category_budget, spending)
    return email_dict

# Get email addresses lookup dict
def get_email_addresses(account_id_array):
    stringified = ', '.join([f"'{ID}'" for ID in account_id_array])
    query = f"SELECT account_id, email FROM [dbo].[Profile] WHERE account_id IN ({stringified})"
    db_dict = query_database(query)
    output = defaultdict(list)
    for row in db_dict['ResultSets']['Table1']:
        output[row.get('account_id')].append(row.get('email'))
    return output

# Get account IDs
account_id_array = get_account_id_array()
# get category budgets
category_budget_dict = get_category_budget_dict()
# create email dict
email_dict = get_email_dict(account_id_array, category_budget_dict)
# Get email lookup dict
account_email_lookup = get_email_addresses(account_id_array)

# Send emails
for (account_id, overspending_dict) in email_dict.items():
    # Construct email body
    email_body = "A gentle reminder! Here's your reminder: \n "
    for (category, budget_spending_tuple) in overspending_dict.items():
        (budget, spending) = budget_spending_tuple
        email_body += f"{category}: budget={budget}, spending={spending} \n"
        
    emails = account_email_lookup.get(account_id)
    for email in emails:
        result = {"email": email, "email_body": email_body}
        url = "https://cloudwars2functionapp.azurewebsites.net/api/TIMERBudgetCategorySendEmail?code=gm1QGHadIAt5vkSuhfygzn0PHKAV1RI69NM4otWJKEGHnS6bVdC/rw=="
        response = requests.post(url=url, json=result)
        print(response)
        