import logging
import azure.functions as func
import json
from adaptivecardbuilder import *
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Log to Azure function apps online
    logging.info('Python HTTP trigger function processed a request.')

    # Try retrieve parameters
    req_body = req.get_json()
    USER_REAL_FACE = req_body.get('user_real_face')
    USER_ID_DOC = req_body.get('user_id_doc')
    
    # Initiate Azure Face api endpoint and key
    ENDPOINT = "https://botcomposerfacialrecognition.cognitiveservices.azure.com"
    API_KEY = "e16448372f3d4996b80bacfd1b93b3bd"
        
    def create_faceid(image_url):
        url = f"{ENDPOINT}/face/v1.0/detect"
        headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": API_KEY}
        body = {"url": image_url}
        response = requests.post(url=url, headers=headers, json=body)
        if response.status_code != 200:
            return func.HttpResponse(body=response.text, status_code=400)
        input_face_id = json.loads(response.text)[0].get('faceId')
        return input_face_id

    # Get face ids
    user_real_face_faceid = create_faceid(USER_REAL_FACE)
    user_id_doc_faceid = create_faceid(USER_ID_DOC)

    def find_similar(user_real_face_faceid, user_id_doc_faceid):
        url = f"{ENDPOINT}/face/v1.0/findsimilars"
        headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": API_KEY}
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
            return jsonified[0].get('confidence')
        else:
            return 0

    # Get similarity confidence
    result = find_similar(user_real_face_faceid, user_id_doc_faceid)
    return func.HttpResponse(body=result, status_code=200)


