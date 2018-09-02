import json
import requests as req
from . import urls

# TODO: implement this class... it's not working at the moment

def executeCurl(*msgs, data:dict=None, localHost:bool=True, reqType:str='POST'):
    for msg in msgs:
        try:
            json:str = None if data == None else json.dumps(data)
        except:
            print("Unable to parse JSON from data.")

        if json == None or reqType == 'GET':
            if reqType == 'POST':
                json = '{"object":"page","entry":[{"id":"1816383528408275","time":1458692752478,"messaging":[{"sender":{"id":"2153980617965043"},"recipient":{"id":"1816383528408275"},"timestamp":1535668107322,"message":{"mid":"BPz5ur9Btq7j4COCe1mCzYkLKYgxzkzkA1c5Qo1fAeHwydq7QZl3h2_9tJsh7t1yWpu-vCymEb1Scci-RVgOkg","seq":1560439,"text":{}}}]}]}'.format(msg)
            elif reqType == 'GET':
                json = 'hub.mode=subscribe&hub.verify_token=OF_MY_APPRECIATION&hub.challenge=challenge_should_be_accepted'
            else: 
                raise ValueError("reqType must be either 'POST' or 'GET'")
        
        url = 'localhost:5000/webhook?' if localHost else urls.MESSAGES_URL

        if reqType == 'POST':
            req.post(url, json=json)
        elif reqType == 'GET':
            req.get(url+json)