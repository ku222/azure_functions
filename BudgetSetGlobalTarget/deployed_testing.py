
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
language = "ms"

def query_database(query):
    logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
    body = {"intent": "query", "params": [query]}
    response = requests.post(url=logic_app_url, json=body)
    return json.loads(response.content)

query = f'''
SELECT SUM(temp_table2.average_monthly_spend) AS average_spending
FROM (
        SELECT temp_table.category, AVG(temp_table.spending) AS average_monthly_spend
        FROM (
            SELECT month(date) AS the_month, Transaction_Category AS category, AVG(WITHDRAWAL_AMT) AS spending
            FROM [dbo].[Transaction_with_category] 
            WHERE account_no = '{account_id}'
            GROUP BY month(date), Transaction_Category
            ) AS temp_table
        GROUP BY temp_table.category
    ) AS temp_table2 
'''
query = query.replace('\n', ' ')
result = query_database(query)
monthly_average = result["ResultSets"]["Table1"][0]["average_spending"]

monthly_average = round(monthly_average, 2)

def create_card(monthly_average, language):
    blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
    whistle_icon = "https://i.ibb.co/vH4BM82/referee.png"

    card = AdaptiveCard(backgroundImage=blue_background)
    card.add([
        Image(url=whistle_icon, height="90px", horizontalAlignment="center", spacing="medium"),
        TextBlock(text="Set Monthly Budget Target", spacing="Large", color="light", size="Large", weight="Bolder", horizontalAlignment="center"),
        ColumnSet(spacing="small"),
            Column(width=1), 
                "<",
            Column(width=15),
                TextBlock(text="Excluding committed costs, whats the most you want to spend this month?", color="light", wrap="true", size="medium", horizontalAlignment="center"),
                Container(style="default", spacing="Large"),
                    Container(spacing="large"),
                        "<",
                    TextBlock(text="Current Monthly Average Spend", size="medium", horizontalAlignment="center"),
                    TextBlock(text=f"${monthly_average:,}", size="ExtraLarge", weight="bolder", horizontalAlignment="center", dont_translate=True),
                    TextBlock(text="Enter maximum spend", spacing="medium", isSubtle="true"),
                    InputNumber(ID="amount", value=800, separator="true", dont_translate=True),
                    ActionSet(),
                        "actions",
                        ActionSubmit(title="Set Spend Target", style="positive"),
                        "<",
                    "<",
                "<",
            "items",
            Column(width=1),
                "<",
            "<",
        ])

    return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")

# Return result
result = create_card(monthly_average, language)
result