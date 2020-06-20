
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

query = f'''
SELECT temp_table.category, AVG(temp_table.spending) AS average_monthly_spend
FROM (
    SELECT month(date) AS the_month, Transaction_Category AS category, AVG(WITHDRAWAL_AMT) AS spending
    FROM [dbo].[Transaction_with_category] 
    WHERE account_no = 'A00003088'
    GROUP BY month(date), Transaction_Category
    ) AS temp_table
GROUP BY temp_table.category
'''

query = query.replace('\n', ' ')
result = query_database(query)

category_averages = {dict_["category"].title():int(dict_["average_monthly_spend"]) for dict_ in result["ResultSets"]["Table1"]}
sum(category_averages.values())

#%%

category_averages

#%%

blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
white_background = "https://www.publicdomainpictures.net/pictures/30000/velka/plain-white-background.jpg"

category_icons = {
    "Groceries": "https://i.pinimg.com/originals/d2/7a/67/d27a6770476cd22bfd2c0abc3d279d5b.png",
    "Banking": "https://i.ibb.co/JRLCCpr/bank.png",
    "Utilities": "https://i.ibb.co/4mpFr1m/iconfinder-utilities-173701.png",
    "Charity": "https://i.ibb.co/mDSL154/heart.png",
    "Employment": "https://i.ibb.co/pv0gGwH/home-office.png",
    "Medical": "https://i.ibb.co/hZpzjZP/virus.png",
    "Travel": "https://i.ibb.co/YyqzCrn/airplane.png",
    "Sports": "https://i.ibb.co/nPwnY2w/trophy.png",
    "Retail": "https://i.ibb.co/DCQ1gXf/market.png",
    "Music": "https://ilandscapeshow.com/wp-content/uploads/2016/07/Entertainment-Icon.png",
    "Accomodation": "https://i.ibb.co/R4Zkp73/bed.png",
    "Restaurant": "https://www.leisurevouchers.co.uk/_common/updateable/category/6fcba5dc-817a-4532-81cf-32192d35ab39.png",
}

sum_categories = sum([v for v in category_averages.values()])
category_percentages = {k:round(v/sum_categories, 2) for (k,v) in category_averages.items()}
category_percentages = {k: v for k, v in sorted(category_percentages.items(), key=lambda item: item[1], reverse=True)}
max_length = 50
budget_target = 800

card = AdaptiveCard(backgroundImage=blue_background)
card.add(Container(backgroundImage=white_background))
container_level = card.save_level()
card.add(TextBlock(text="Set Monthly Category Budgets", size="ExtraLarge", weight="lighter", horizontalAlignment="center"))
for (category, perc) in category_percentages.items():
    card.load_level(container_level)
    num_units = int(max_length * perc)
    target_units = int((budget_target/sum_categories)*num_units)
    average = category_averages[category]
    card.add([
        ColumnSet(separator="true", spacing="medium"),
            Column(width=1, verticalContentAlignment="center"),
                Image(url=category_icons[category]),
                "<",
            Column(width=6),
                ColumnSet(),
                    Column(verticalContentAlignment="top"),
                        TextBlock(text=category, weight="bolder", size="medium"),
                        "<",
                    "<",
                ColumnSet(),
                    Column(width=1, verticalContentAlignment="top"),
                        TextBlock(text="Current", color="attention", size="small"),
                        "<",
                    Column(width=3, verticalContentAlignment="top"),
                        TextBlock(text=f"{chr(9608)*num_units}", color="attention", size="small"),
                        "<",
                    Column(width=1, verticalContentAlignment="top"),
                        TextBlock(text=f"{int(perc*100)}%"),
                        "<",
                    Column(width=1, verticalContentAlignment="top"),
                        TextBlock(text=f"${average:,}"),
                        "<",
                    "<",
                ColumnSet(),
                    Column(width=1, verticalContentAlignment="top"),
                        TextBlock(text="Target", color="accent", size="small"),
                        "<",
                    Column(width=3, verticalContentAlignment="top"),
                        TextBlock(text=f"{chr(9608)*target_units}", color="accent", size="small"),
                        "<",
                    Column(width=1, verticalContentAlignment="top"),
                        "<",
                    Column(width=1, verticalContentAlignment="top"),
                        TextBlock(text=f"${int(perc*budget_target):,}"),
                        "<",
                    "<",
                "<",
            "<",
        ColumnSet(),
            Column(width=1, verticalContentAlignment="center"),
                "<",
            Column(width=1, verticalContentAlignment="center"),
                TextBlock(text="Target: $", horizontalAlignment="left", color="accent", size="small"),
                "<",
            Column(width=5, verticalContentAlignment="center"),
                InputNumber(ID=category, placeholder=perc*budget_target, value=perc*budget_target)
    ])

# Now add global submit
card.back_to_top()
card.add(ActionSubmit(title="Set Category Targets", style="positive"), is_action="true")
    
card.to_json().replace("\\u2588", chr(9608))

#%%
blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
whistle_icon = "https://i.ibb.co/vH4BM82/referee.png"
monthly_average = 455.44

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
                TextBlock(text=f"${monthly_average:,}", size="ExtraLarge", weight="bolder", horizontalAlignment="center"),
                TextBlock(text="Enter maximum spend", spacing="medium", isSubtle="true"),
                InputNumber(ID="amount", value=800, separator="true"),
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

card.to_json()


#%%

import numpy as np 

a = np.random.rand(64, 56)

a[:,:]
