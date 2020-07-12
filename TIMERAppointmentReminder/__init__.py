import datetime
import logging

import json
import requests
import random
from collections import defaultdict

import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    
    def query_database(query):
        logic_app_url = "https://prod-20.uksouth.logic.azure.com:443/workflows/c1fa3f309b684ba8aee273b076ee297e/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=xYEHzRLr2Frof9x9_tJYnif7IRWkdfxGC5Ys4Z3Jkm4"
        body = {"intent": "query", "params": [query]}
        response = requests.post(url=logic_app_url, json=body)
        return json.loads(response.content)

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
        return translated_output
        
    def get_appointments():
        query = f'''
        SELECT profile.first, profile.email, profile.LanguagePreference, appt.branch_name, appt.start_time, appt.end_time
        FROM CustomerAppointments AS appt
        LEFT JOIN Profile AS profile
        ON appt.account_id = profile.account_id
        WHERE reminder_sent = 0
        '''
        db_dict = query_database(query.replace('\n', ' '))
        output = []
        rows = db_dict['ResultSets']['Table1']
        for row_dict in rows:
            values = list(row_dict.values())
            output.extend(values)
        return output

    def to_datetime(hrs_mins):
        return datetime.datetime.strptime(hrs_mins, '%H:%M:%S')


    # Create appointments list
    appointments = get_appointments()
    
    # Send emails
    for (first_name, email_address, language_preference, branch_name, appt_start, appt_end) in appointments:
        # Check if its < 3 hours before the appointment
        now = datetime.datetime.now()
        hrs_mins_now = to_datetime(f"{now.hour}:{now.minute}:{now.second}")
        appt_start_time_object = to_datetime(appt_start)
        # exit if we've already passed the start time
        if now > appt_start_time_object:
            continue 
        # exit if not within 3 hours
        is_within_3_hours = (appt_start_time_object - hrs_mins_now).seconds/3600 <= 3
        if not is_within_3_hours:
            continue
        
        # Else construct email body
        email_body = [f"Hello {first_name}! It's Lingo from the Bank of Lingfield! I'm sending you a friendly reminder about your appointment!:"]
        email_body.append(f"You've got an appointment at {branch_name}, from {appt_start} to {appt_end}")
        email_body.append("Traffic looks busy, so remember to leave early!")
        email_body.append("Lots of love from your pal,")
        email_body.append("Lingo")
        
        # Translate email body first
        if language_preference != 'en':
            email_body = translate_list_of_strings(string_list=email_body, to_lang=language_preference)
        result = {"email": email_address, "email_body": '\n.'.join(email_body)}
        url = "https://cloudwars2functionapp.azurewebsites.net/api/TIMERBudgetCategorySendEmail?code=gm1QGHadIAt5vkSuhfygzn0PHKAV1RI69NM4otWJKEGHnS6bVdC/rw=="
        requests.post(url=url, json=result)