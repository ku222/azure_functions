import logging
import azure.functions as func
import json
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
 
    req_body = req.get_json()
    code = req_body.get('code')
    
    code_to_lang = {
        'af': 'Afrikaans',
        'ar': 'Arabic',
        'bn': 'Bangla',
        'bs': 'Bosnian (Latin)',
        'bg': 'Bulgarian',
        'yue': 'Cantonese (Traditional)',
        'ca': 'Catalan',
        'zh-Hans': 'Chinese Simplified',
        'zh-Hant': 'Chinese Traditional',
        'hr': 'Croatian',
        'cs': 'Czech',
        'da': 'Danish',
        'nl': 'Dutch',
        'en': 'English',
        'et': 'Estonian',
        'fj': 'Fijian',
        'fil': 'Filipino',
        'fi': 'Finnish',
        'fr': 'French',
        'de': 'German',
        'el': 'Greek',
        'gu': 'Gujarati',
        'ht': 'Haitian Creole',
        'he': 'Hebrew',
        'hi': 'Hindi',
        'mww': 'Hmong Daw',
        'hu': 'Hungarian',
        'is': 'Icelandic',
        'id': 'Indonesian',
        'ga': 'Irish',
        'it': 'Italian',
        'ja': 'Japanese',
        'kn': 'Kannada',
        'kk': 'Kazakh',
        'sw': 'Kiswahili',
        'tlh-Latn': 'Klingon',
        'tlh-Piqd': 'Klingon (plqaD)',
        'ko': 'Korean',
        'lv': 'Latvian',
        'lt': 'Lithuanian',
        'mg': 'Malagasy',
        'ms': 'Malay',
        'ml': 'Malayalam',
        'mt': 'Maltese',
        'mi': 'Maori',
        'mr': 'Marathi',
        'nb': 'Norwegian',
        'fa': 'Persian',
        'pl': 'Polish',
        'pt-br': 'Portuguese (Brazil)',
        'pt-pt': 'Portuguese (Portugal)',
        'pa': 'Punjabi',
        'otq': 'Queretaro Otomi',
        'ro': 'Romanian',
        'ru': 'Russian',
        'sm': 'Samoan',
        'sr-Cyrl': 'Serbian (Cyrillic)',
        'sr-Latn': 'Serbian (Latin)',
        'sk': 'Slovak',
        'sl': 'Slovenian',
        'es': 'Spanish',
        'sv': 'Swedish',
        'ty': 'Tahitian',
        'ta': 'Tamil',
        'te': 'Telugu',
        'th': 'Thai',
        'to': 'Tongan',
        'tr': 'Turkish',
        'uk': 'Ukrainian',
        'ur': 'Urdu',
        'vi': 'Vietnamese',
        'cy': 'Welsh',
        'yua': 'Yucatec Maya'
        }

    result = code_to_lang.get(code)
    return func.HttpResponse(body=result, status_code=200)

