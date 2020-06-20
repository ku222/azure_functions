import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Try retrieve params
    req_body = req.get_json()
    user_real_face = req_body.get('user_face')
    user_id = req_body.get('user_id')
    
    # Initiate Azure Face api endpoint and key
    endpoint = "https://botcomposerfacialrecognition.cognitiveservices.azure.com"
    api_key = "e16448372f3d4996b80bacfd1b93b3bd"
    
    def create_faceid(image_url, endpoint=endpoint, api_key=api_key):
        url = f"{endpoint}/face/v1.0/detect"
        headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": api_key}
        body = {"url": image_url}
        response = requests.post(url=url, headers=headers, json=body)
        if response.status_code != 200:
            return func.HttpResponse(body=response.text, status_code=400)
        input_face_id = json.loads(response.text)[0].get('faceId')
        return input_face_id

    # Get face ids
    user_real_face_faceid = create_faceid(user_real_face)
    user_id_doc_faceid = create_faceid(user_id)

    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    def find_similar(user_real_face_faceid, user_id_doc_faceid, endpoint=endpoint, api_key=api_key):
        url = f"{endpoint}/face/v1.0/findsimilars"
        headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": api_key}
        body = {
            "faceId": user_real_face_faceid,
            "faceIds": [user_id_doc_faceid],
            "maxNumOfCandidatesReturned": 5,
            "mode": "matchPerson"
            }
        response = requests.post(url=url, headers=headers, json=body)
        if response.status_code != 200:
            return func.HttpResponse(body=response.text, status_code=400)
        jsonified = json.loads(response.text)
        if jsonified:
            return str(jsonified[0].get('confidence'))
        else:
            return str(0)

    # Get similarity confidence
    result = find_similar(user_real_face_faceid, user_id_doc_faceid)
    return func.HttpResponse(body=result, status_code=200)


