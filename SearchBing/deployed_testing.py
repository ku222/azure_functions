
#%%

import requests
import json
from adaptivecardbuilder import *


language = 'ms'

def search_bing(query):
    endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    headers = {'Ocp-Apim-Subscription-Key': '95a2b791f29547a59d7a2d4ba5c8ccde'}
    params = {
        'q': query,
        'count': '3',
        'offset': '0',
        'mkt': 'en-us',
        'safesearch': 'Moderate',
    }
    response = requests.get(url=endpoint, headers=headers, params=params)
    results_dict = response.json()
    return results_dict

# List -> value['contentUrl'] in response.json()['images']['value']

def display_results(results_dict, language):
    blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
    card = AdaptiveCard(backgroundImage=blue_background)
    
    # First add the webpage information
    for result in results_dict['webPages']['value']:
        card.add([
            Container(style="default"),
                TextBlock(text=result['name'], size="large", weight="bolder"),
                TextBlock(text=result['displayUrl'], size="small", isSubtle="true", wrap="true"),
                TextBlock(text=result['snippet'], wrap="true", spacing="medium"),
                ActionSet(),
                    "action",
                    ActionOpenUrl(url=result['url'], title="Go to Website", style="positive"),
                    "items",
        "^",
        ])
    
    # Now add image information
    if results_dict.get('images'):
        card.add(ImageSet(spacing="Large", separator="true", imageSize="medium"))
        for result in results_dict['images']['value']:
            card.add(Image(url=result['contentUrl'], selectAction={"type": "Action.OpenUrl", "url": result['contentUrl']}))
        
    return card.to_json()

display_results(results_dict, 'en')


#%%
results_dict = search_bing('bus stops around here')


#%%

display_results(results_dict, language="en")