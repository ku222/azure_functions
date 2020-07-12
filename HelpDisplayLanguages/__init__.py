import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:

    req_body = req.get_json()
    language = req_body.get('language')

    def create_card(language):
        blue_background = "https://digitalsynopsis.com/wp-content/uploads/2017/02/beautiful-color-gradients-backgrounds-047-fly-high.png"
        white_background = "https://i.pinimg.com/originals/f5/05/24/f50524ee5f161f437400aaf215c9e12f.jpg"
        lang_to_code = {
            'Afrikaans': 'af',
            'Arabic': 'ar',
            'Bangla': 'bn',
            'Bosnian (Latin)': 'bs',
            'Bulgarian': 'bg',
            'Cantonese (Traditional)': 'yue',
            'Catalan': 'ca',
            'Chinese Simplified': 'zh-Hans',
            'Chinese Traditional': 'zh-Hant',
            'Croatian': 'hr',
            'Czech': 'cs',
            'Danish': 'da',
            'Dutch': 'nl',
            'English': 'en',
            'Estonian': 'et',
            'Fijian': 'fj',
            'Filipino': 'fil',
            'Finnish': 'fi',
            'French': 'fr',
            'German': 'de',
            'Greek': 'el',
            'Gujarati': 'gu',
            'Haitian Creole': 'ht',
            'Hebrew': 'he',
            'Hindi': 'hi',
            'Hmong Daw': 'mww',
            'Hungarian': 'hu',
            'Icelandic': 'is',
            'Indonesian': 'id',
            'Irish': 'ga',
            'Italian': 'it',
            'Japanese': 'ja',
            'Kannada': 'kn',
            'Kazakh': 'kk',
            'Kiswahili': 'sw',
            'Klingon': 'tlh-Latn',
            'Klingon (plqaD)': 'tlh-Piqd',
            'Korean': 'ko',
            'Latvian': 'lv',
            'Lithuanian': 'lt',
            'Malagasy': 'mg',
            'Malay': 'ms',
            'Malayalam': 'ml',
            'Maltese': 'mt',
            'Maori': 'mi',
            'Marathi': 'mr',
            'Norwegian': 'nb',
            'Persian': 'fa',
            'Polish': 'pl',
            'Portuguese (Brazil)': 'pt-br',
            'Portuguese (Portugal)': 'pt-pt',
            'Punjabi': 'pa',
            'Queretaro Otomi': 'otq',
            'Romanian': 'ro',
            'Russian': 'ru',
            'Samoan': 'sm',
            'Serbian (Cyrillic)': 'sr-Cyrl',
            'Serbian (Latin)': 'sr-Latn',
            'Slovak': 'sk',
            'Slovenian': 'sl',
            'Spanish': 'es',
            'Swedish': 'sv',
            'Tahitian': 'ty',
            'Tamil': 'ta',
            'Telugu': 'te',
            'Thai': 'th',
            'Tongan': 'to',
            'Turkish': 'tr',
            'Ukrainian': 'uk',
            'Urdu': 'ur',
            'Vietnamese': 'vi',
            'Welsh': 'cy',
            'Yucatec Maya': 'yua'
            }
        card = AdaptiveCard(backgroundImage=blue_background)
        card.add(Container(backgroundImage=white_background))
        container_level = card.save_level()
        for (lang, lang_code) in lang_to_code.items():
            card.add([
                "items",
                ColumnSet(separator="true"),
                    Column(),
                        TextBlock(text=lang),
                        "<",
                    Column(),
                        ActionSet(),
                            "action",
                            ActionSubmit(title="Speak This!", style="positive", data=dict(action=lang_code)),
            ])
            card.load_level(container_level)
        
        if language == 'en':
            return card.to_json()
        return card.to_json(translator_to_lang=language, translator_key="e8662f21ef0646a8abfab4f692e441ab")

    result = create_card(language)
    return func.HttpResponse(body=result, status_code=200)

