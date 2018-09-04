
import json
import logging
import os

from typing import (Tuple, Union)
from wit import Wit

from ...scripts import attachMapToMessenger as bartMap
from ...utils import phrases
from ...utils.keys import WIT_TOK
from ...utils.requests import (get, post)
from ...utils.urls import (AUTH, GRAPH_API, MESSAGES_API, MESSENGER_USER_API)


MAP_ID = "264370450851085"

def handle_message(fbId:str, message:dict) -> str:
    logging.debug("Message: {}".format(json.dumps(message,indent=2)))
    res:str = "test"
    if 'text' in message.keys():
        res = handle_text(fbId, message['text'])
    elif 'attachments' in message.keys():
        res = handle_attachment(fbId, message['attachments'])
    else: 
        logging.warning("Received empty message event")
        res = "Message body is empty."

    return res


def handle_attachment(fbId:str, attach:dict) -> str:
    logging.info("Received attachment message event")
    return 'OK'


def handle_text(fbId:str, text:str) -> str:
    logging.info("Received text message event")
    logging.debug("Message: {}".format(text))

    nlp_entities:dict = get_wit_entities(fbId, text)

    if nlp_entities == None:
        # TODO: Create fallback, either message about NLP or do cheap hack
        # TODO: Link to another suitable BART schedule thing. 
            # Maybe download offline schedules if can't access BART API
        return "Cannot access Wit at the moment."

    entities:dict = nlp_entities['entities']

    # HACK: fix entity parsing
    fn,ln = get_id_name(fbId)
    if 'greeting' in entities:
        logging.info('Sending a greeting')
        text = phrases.get_phrase(phrases.hello,phrases.cta).format(fn=fn)
    elif 'intent' in entities and 'map' == entities['intent'][0]['value']:
        text = send_map(fbId, fn)
    else:
        text = "Hello {} {}. You typed: ".format(fn,ln) + nlp_entities['_text']
    
    text += "\nDebug info: {}".format(json.dumps(entities, indent=4))

    return fb_message(fbId, text)


def send_map(fbId:str, fn:str='{opt}') -> str:
    """Sends a map using Messenger Attachment and returns delivery phrase"""
    logging.info('Sending a map')
    logging.debug('fbId: {}'.format(fbId))
    mapId = bartMap.get_map_id()
    if mapId != None: 
        data = {
            'recipient': {'id': fbId},
            'messaging_type': 'RESPONSE',
            'message': {
                'attachment': {
                    'type': 'image',
                    'payload': {
                        'attachment_id': mapId}}}}
        post(MESSAGES_API, json=data)
        return phrases.get_phrase(phrases.delivery, opt=fn)
    else: 
        # HACK: Make this better
        return 'Check here! http://www.bart.gov/stations'


def fb_message(fbId:str, text:str) -> str:
    """Returns response to Messenger via Send API"""

    logging.info("Sending message '{text}' to FB ID {id}".format(text=text,id=fbId))
    data = {
        'messaging_type': 'RESPONSE',
        'recipient': {'id': fbId},
        'message': {'text': text}}
    post(MESSAGES_API, json=data)
    return 'OK'


def get_id_name(fbId:str) -> Tuple[str,str]:
    """
    Requests first and last name of ID from Messenger User Profile API
    https://developers.facebook.com/docs/messenger-platform/identity/user-profile/
    """

    logging.info("Getting FB name")
    queries = {'fields':['first_name','last_name']}
    ok, data = get(MESSENGER_USER_API.format(fbId=fbId),json=queries)
    if "error" in data.keys():
        return ('{fn}','{ln}')
    else: 
        return (data['first_name'], data['last_name'])


def get_wit_entities(fbId:str, text:str) -> Union[None,str]:
    """Calls Wit API for natural language processing"""
    try:
        resp = Wit(access_token=WIT_TOK).message(
            msg=text, context={'session_id':fbId}, verbose=True)
        logging.info("Retrieved Wit entities")
        logging.debug("Wit entities: {}".format(json.dumps(resp,indent=2)))
        return resp
    except Exception as e:
        logging.error("Failed to access Wit API. Error: {}.".format(e))
        return None



# TODO: For unsure traits, offer a "find nearest" button

# TODO: Implement "yes/no" postback quick replies
#   Vary the "yes/no" e.g. "yes!/no...", "affirmative/negatory", "yep/nope"