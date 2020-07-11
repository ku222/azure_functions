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
    language = req_body.get('language')
    
    # Translation Function
    def translate_list_of_strings(string_list, to_lang):
        base_url="https://api.cognitive.microsofttranslator.com/translate?api-version=3.0"
        translator_key="e8662f21ef0646a8abfab4f692e441ab"
        headers = {
            "Ocp-Apim-Subscription-Key": translator_key,
            "Content-Type": "application/json; charset=UTF-8",
            "Content-Length": str(len(string_list))
            }
        # Construct body
        body = [{"Text": text} for text in string_list]
        # Post request, return
        response = requests.post(url=f"{base_url}&to={to_lang}", headers=headers, json=body)
        # Extract translations
        translated_output = []
        for response_dict in response.json():
            translations_array = response_dict['translations']
            first_result = translations_array[0]
            translated_text = first_result['text']
            translated_output.append(translated_text)
        return translated_output[0]
    
    result = translate_list_of_strings([message], to_lang=language)
    return func.HttpResponse(body=result, status_code=200)

