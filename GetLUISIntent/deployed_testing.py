
#%%

import requests
import json


#%% Example payload in dict form
# u'\u2588'

app_id = "9117b808-1323-4b13-aed4-47d4b6fa6a04"
authoring_key = "f941aa60cf67403fa1b7a528a613993b"
prediction_endpoint = "https://westeurope.api.cognitive.microsoft.com/"
utterance = "Yes Please"
parameters = {
    'query': utterance,
    'timezoneOffset': '0',
    'verbose': 'true',
    'show-all-intents': 'true',
    'spellCheck': 'false',
    'staging': 'false',
    'subscription-key': authoring_key
}

