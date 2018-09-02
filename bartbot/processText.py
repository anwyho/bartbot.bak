import json
import logging as log
from typing import Tuple, Union

import requests as req

from wit import Wit

from . import keys as k
from . import phrases
from .urls import AUTH, GRAPH_API, MESSAGES_URL


def handle_attachment(fbId:str, attach:dict) -> str:
    return 'OK'


def handle_text(fbId:str, text:str) -> str:
    nlp_entities:dict = get_wit_entities(fbId, text)
    if nlp_entities == None:
        # TODO: Create fallback, either message about NLP or do cheap hack
        # TODO: Link to another suitable BART schedule thing. 
        pass

    entities:dict = nlp_entities['entities']
    # Checks if user's message is a greeting
    # Otherwise we will just repeat what they sent us
    greetings:str = first_entity_value(entities, 'greetings')
    fn,ln = get_id_name(fbId)
    if greetings:
        text = phrases.get_phrase(phrases.hello,phrases.cta).format(fn=fn)
    else:
        text = "Hello {} {}. You typed: ".format(fn,ln) + nlp_entities['_text']
    
    text += "\nDebug info: {}".format(json.dumps(entities, indent=4))

    return fb_message(fbId, text)


def fb_message(fbId:str, text:str) -> str:
    """Function for returning response to messenger"""
    log.info("Sending message {text} to FB ID {id}".format(text=text,id=fbId))
    
    data = {
        'messaging_type': 'RESPONSE',
        'recipient': {'id': fbId},
        'message': {'text': text}}
    
    resp = req.post(MESSAGES_URL, json=data)
    handle_errors(resp)
    return 'OK'



    

def handle_errors(response:dict):
    log.debug("Response: {}".format(json.dumps(response.json())))


def get_id_name(fbId:str) -> Tuple[str,str]:
    log.info("Getting FB name")
    q = {'fields':['first_name','last_name']}
    resp = req.get(GRAPH_API+fbId+'?'+AUTH, json=q)
    data = resp.json()
    if "error" in data.keys():
        return None
    else: 
        return (data['first_name'], data['last_name'])


def get_wit_entities(fbId:str, text:str) -> Union[None,str]:
    # TODO: log the wit entities with a json dump
    try:
        return Wit(access_token=k.WIT_TOK).message(
            msg=text, context={'session_id':fbId}, verbose=True)
    except Exception as e:
        log.error("Failed to access Wit API. Error: {}".format(e))
        return None

def first_entity_value(entities, entity):
    """Returns first entity value"""
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val




def turn_on_seen_and_typing_indicator(fbId:str):
    """POST to Messenger Platform to turn on sender actions"""
    data = {
        'messaging_type': 'RESPONSE', 
        'recipient': { 'id': fbId }}

    data['sender_action'] = 'mark_seen'
    resp = req.post(MESSAGES_URL, json=data)
    handle_errors(resp)
    data['sender_action'] = 'typing_on'
    resp = req.post(MESSAGES_URL, json=data)
    handle_errors(resp)
