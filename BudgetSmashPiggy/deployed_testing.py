
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

account_id = 'A00003088'
piggybank_name = "Holiday"
piggybank_amount = "1000.40"
created_date = "01/01/2020"
date_today = str(date.today())
language = 'ms'

def create_card(piggybank_name, piggybank_amount, created_date, date_today, language):
    blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
    piggy_icon = "https://i.ibb.co/sKfW8Nd/debt.png"

    card = AdaptiveCard(backgroundImage=blue_background)
    card.add([
        TextBlock(text=f"Here lies", color="light", size="ExtraLarge", weight="Bolder", horizontalAlignment="center"),
        RichTextBlock(horizontalAlignment="center"),
            TextRun(text=f"Good Old ", color="light", size="Large", wrap="true"),
            TextRun(text=f"{piggybank_name}", color="light", size="Large", wrap="true", dont_translate=True),
            TextRun(text=f" Piggy Bank", color="light", size="Large", wrap="true"),
            "<",
        TextBlock(text=f"Who Amounted to ${piggybank_amount:,}", color="light", size="Medium", wrap="true", horizontalAlignment="center"),
        
        ColumnSet(separator="true", spacing="Large"),
            Column(),
                TextBlock(text=f"Born", color="light", separator="true", size="Large", weight="bolder", spacing="Large", wrap="true", horizontalAlignment="center"),
                TextBlock(text=f"{created_date}", color="light", size="Large", wrap="true", horizontalAlignment="center", dont_translate=True),
                "<",
            Column(),
                TextBlock(text=f"Smashed", color="light", size="Large", weight="bolder", spacing="Large", wrap="true", horizontalAlignment="center"),
                TextBlock(text=f"{date_today}", color="light", size="Large", wrap="true", horizontalAlignment="center", dont_translate=True),
                "<",
            "<",
        
        Image(url=piggy_icon, spacing="Large", height="200px", horizontalAlignment="center"),
        
    ])
    return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")

# Create card
result = create_card(piggybank_name=piggybank_name, piggybank_amount=float(piggybank_amount), created_date=created_date, date_today=date_today, language=language)
    
#%%
result
