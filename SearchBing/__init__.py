import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:

    req_body = req.get_json()
    message = req_body.get('message')
    language = req_body.get('language')
    
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

    def display_results(results_dict, language):
        blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
        card = AdaptiveCard(backgroundImage=blue_background)
        
        # First add the webpage information
        for result in results_dict['webPages']['value']:
            card.add([
                Container(backgroundImage="https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg"),
                    TextBlock(text=result['name'], size="large", weight="bolder"),
                    TextBlock(text=result['displayUrl'], size="small", isSubtle="true", wrap="true"),
                    TextBlock(text=result['snippet'], wrap="true", spacing="medium"),
                    ActionSet(),
                        "action",
                        ActionOpenUrl(url=result['url'], title="Go to Website", style="positive"),
                        "items",
            "^",
            ])
        
        # Now add image information if applicable
        if results_dict.get('images'):
            card.add(ImageSet(spacing="Large", separator="true", imageSize="medium"))
            for result in results_dict['images']['value']:
                card.add(Image(url=result['contentUrl'], selectAction={"type": "Action.OpenUrl", "url": result['contentUrl']}))
        
        if language == 'en':
            return card.to_json()
        return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")
    
    results_dict = search_bing(message)
    result = display_results(results_dict, language)
    return func.HttpResponse(body=result, status_code=200)


