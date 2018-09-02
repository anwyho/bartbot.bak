# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
# from __future__ import unicode_literals

import json
import logging as log
import os
import random
import requests as req
import sys

from flask import Flask, request, redirect, url_for
from typing import Tuple, Union
from wit import Wit

from . import keys as k
from . import phrases


# URLs
GRAPH_API: str = 'https://graph.facebook.com/'
MESSENGER_PLATFORM: str = GRAPH_API+'v2.6/me/'
AUTH: str = 'access_token={token}&appsecret_proof={proof}'.format(
    token=k.FB_PAGE_ACCESS,
    proof=k.gen_app_secret_proof())
MESSAGES_URL: str = MESSENGER_PLATFORM+'messages?'+AUTH


def pre_response(fbId:str, messageObj:dict) -> None:
    """Tasks to prep for and set up response"""
    turn_on_seen_and_typing_indicator(fbId)

def post_response(result:str, fbId:str, messageObj:dict) -> str:
    """Tasks to clean up response before returning"""
    return result

def process_messages_event(req) -> str:
    """Handler for webhook (currently for postback and messages)"""
    try:  # parse JSON into data
        data:dict = req.json
    except Exception as e:
        log.warning("Couldn't parse JSON with req.json.")
        return "Unable to parse JSON."
    
    try:  # validate and extract data from JSON for parsing
        if data['object'] != 'page':
            raise KeyError(
                "Expected 'page' object, received '{}' object".format(
                    data['object']))

        if not 'entry' in data.keys():
            raise KeyError("Expected 'entry' in request object.")

        for entry in data['entry']:
            if not 'messaging' in entry:
                raise KeyError("Expected 'messaging' in entry")
            process_entry(entry)
    except KeyError as e:
        log.warning(
            "Couldn't parse JSON structure. Received error: {}.".format(e))
        return "Unexpected JSON structure."
    except Exception as e:
        log.error("An unexpected error occurred. Error: {}.".format(e))
        return "Not OK, but surviving. Check logs."
    return res


def process_entry(entry:dict):
    for m in entry['messaging']:
        try: 
            fbId:str = m['sender']['id']
        except:
            raise KeyError("Expected 'sender.id' in messaging") 

        pre_response(fbId, m['message'])

        res:str = None
        if 'text' in m['message'].keys():
            log.info("Received text event.")
            res = handle_text(fbId, m['message']['text'])
        elif 'attachments' in m['message'].keys():
            log.info("Received attachment event.")
            res = handle_attachment(fbId, m['message']['attachments'])
        else: 
            log.warning("Received empty event.")
            res = "Message body is empty."
        
        res = post_response(res, fbId, m['message'])


def handle_attachment(fbId:str, attach:dict):
    return 'OK'


def handle_text(fbId:str, text:str):
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
        text = "Hello {}!".format(fn)
    else:
        text = "Hello {} {}. You typed: ".format(fn,ln) + response['_text']

    fb_message(fbId, text)

    return 'OK'


def get_wit_entities(fbId:str, text:str) -> Union[None,str]:
    try:
        return Wit(access_token=k.WIT_TOK).message(
            msg=text, context={'session_id':fbId}, verbose=True)
    except Exception as e:
        log.error("Failed to access Wit API. Error: {}".format(e))
        return None


def fb_message(fbId:str, text:str):
    """Function for returning response to messenger"""
    data = {
        'messaging_type': 'RESPONSE',
        'recipient': {'id': fbId},
        'message': {'text': text}}
    
    resp = req.post(MESSAGES_URL, json=data)
    handle_errors(resp)


def first_entity_value(entities, entity):
    """Returns first entity value"""
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def turn_on_seen_and_typing_indicator(fbId):
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
    

def handle_errors(response):
    pass


def get_id_name(fbId:str) -> Tuple[str,str]:
    q = {'fields':['first_name','last_name']}
    resp = req.get(GRAPH_API+fbId+'?'+AUTH, json=q)
    data = resp.json()
    if "error" in data.keys():
        return None
    else: 
        return (data['first_name'], data['last_name'])


# TODO: for unsure traits, offer a "find nearest" button