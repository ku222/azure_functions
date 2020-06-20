
#%%

import requests
import json

user_real_face = "https://img.ti-media.net/wp/uploads/sites/46/2020/02/New-Project-2020-02-05T124104.465-920x518.jpg"
user_id = "https://images.wsj.net/im-132147?width=620&size=1.5"

DEPLOYED_URL = 'https://cloudwars2functionapp.azurewebsites.net/api/OnboardingFaceMatching?code=aujwEUoc/kwwLk0tPdGKFa0L3P12FEDF36gog5t/gHJ90IQLUY9Veg=='
json_payload = {
    "user_face": user_real_face,
    "user_id": user_id
    }
response = requests.post(url=DEPLOYED_URL, json=json_payload)
response.text

#%% Example payload in dict form


# Initiate Azure Face api endpoint and key
endpoint = "https://botcomposerfacialrecognition.cognitiveservices.azure.com"
api_key = "e16448372f3d4996b80bacfd1b93b3bd"

def create_faceid(image_url, endpoint=endpoint, api_key=api_key):
    url = f"{endpoint}/face/v1.0/detect"
    headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": api_key}
    body = {"url": image_url}
    response = requests.post(url=url, headers=headers, json=body)
    try:
        input_face_id = json.loads(response.text)[0].get('faceId')
    except IndexError:
        return None
    return input_face_id

def find_similar(user_real_face_faceid, user_id_doc_faceid, endpoint=endpoint, api_key=api_key):
    result = 0
    url = f"{endpoint}/face/v1.0/findsimilars"
    headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": api_key}
    body = {
        "faceId": user_real_face_faceid,
        "faceIds": [user_id_doc_faceid],
        "maxNumOfCandidatesReturned": 5,
        "mode": "matchPerson"
        }
    response = requests.post(url=url, headers=headers, json=body)
    jsonified = json.loads(response.text)
    if jsonified:
        result = str(jsonified[0].get('confidence'))
    return result

# Get face ids
user_real_face_faceid = create_faceid(user_real_face)
user_id_doc_faceid = create_faceid(user_id)

if not user_real_face_faceid or not user_id_doc_faceid:
    return func.HttpResponse(body=str(0), status_code=200)

# Get similarity confidence
result = find_similar(user_real_face_faceid, user_id_doc_faceid)

#%%
# Get similarity confidence
result = find_similar(user_real_face_faceid, user_id_doc_faceid)