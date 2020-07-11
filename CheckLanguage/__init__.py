import logging
import azure.functions as func
import json
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve account number
    req_body = req.get_json()
    message = req_body.get('message')
    
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
    
    def detect_language(string_list, translator_key="e8662f21ef0646a8abfab4f692e441ab"):
        base_url="https://api.cognitive.microsofttranslator.com/detect?api-version=3.0"
        translator_key="e8662f21ef0646a8abfab4f692e441ab"
        headers = {
            'Ocp-Apim-Subscription-Key': translator_key,
            'Content-type': 'application/json',
        }
        # Construct body
        body = [{"Text": text} for text in string_list]
        # Post request, return
        response = requests.post(url=base_url, headers=headers, json=body)
        # Extract translations
        return response.json()[0].get('language')
    
    lang_code = detect_language([message])
    lang = code_to_lang[lang_code]
    result = json.dumps([lang, lang_code])
    return func.HttpResponse(body=result, status_code=200)

