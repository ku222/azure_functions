
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

account_id = 'A00000001'

def query_database(query):
    logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
    body = {"intent": "query", "params": [query]}
    response = requests.post(url=logic_app_url, json=body)
    return json.loads(response.content)

# Retrieve account balance
db_dict = query_database(f"SELECT balance from [dbo].[Profile] WHERE account_id = '{account_id}'")
balance = db_dict['ResultSets']['Table1'][0]['balance']
balance
#%%

date 
#%% Creation Page
from adaptivecardbuilder import *
import requests
import json

blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
bot_icon = "https://i.ibb.co/bNsd8SG/LingoBot.png"
purpley_background = "https://images.unsplash.com/photo-1557683311-eac922347aa1?ixlib=rb-1.2.1&w=1000&q=80"
user_name = "Coleman"

card = AdaptiveCard(backgroundImage=purpley_background)
card.add(Image(url=bot_icon, height="200px", horizontalAlignment="center"))
card.add(TextBlock(text=f"Welcome Back, {user_name}!", spacing="Large", weight="bolder", size="ExtraLarge", horizontalAlignment="center", color="light"))
card.add(TextBlock(text="Im Lingo, your very own personal banking assistant.", wrap="true", spacing="medium", size="medium", horizontalAlignment="center", color="light" ))
card.add(TextBlock(text="Here are some things you can ask me to help you with...", wrap="true", spacing="medium", horizontalAlignment="center", color="light" ))

card.to_json()


#%%

for 