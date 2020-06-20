
#%%

import requests
import json

user_real_face = "https://i.pinimg.com/originals/7b/e0/4e/7be04e14777c66806b5f230715cb19cd.png"
user_id = "https://i.pinimg.com/originals/7b/e0/4e/7be04e14777c66806b5f230715cb19cd.png"

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/OnboardingFaceMatching?code=aujwEUoc/kwwLk0tPdGKFa0L3P12FEDF36gog5t/gHJ90IQLUY9Veg=='
json_payload = {
    "user_face": "https://i.pinimg.com/originals/7b/e0/4e/7be04e14777c66806b5f230715cb19cd.png",
    "user_id": "https://i.pinimg.com/originals/7b/e0/4e/7be04e14777c66806b5f230715cb19cd.png"
    }
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%% Example payload in dict form

