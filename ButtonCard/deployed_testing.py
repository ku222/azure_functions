
#%%

import requests
import json

prompt = "Type a 4-digit pin below"
placeholder = "Type here"
submit_title = "Reset my PIN"

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/InputCard?code=8PxznKG3yJ02hoLcqUliERBqDqXq4M231LOvy9Je9qh73kqWunJx6w=='
json_payload = {'prompt': prompt, 'placeholder': placeholder, 'submit_title': submit_title}
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%% Example payload in dict form

prompt = "Type name here"
placeholder = "A name"
submit_title = "Submit!"
language = "ms"

def create_card(prompt, placeholder, submit_title, language):
    card = AdaptiveCard()
    
    card.add([
        "items",
        TextBlock(text=prompt, weight="Bolder", separator="true"),
        InputText(ID="input", placeholder=placeholder),
        
        "Actions",
        ActionSubmit(title=submit_title)
    ])
                    
    return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")

result = create_card(prompt, placeholder, submit_title, language)


# %%
result