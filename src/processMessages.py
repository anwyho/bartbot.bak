from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import os
import random
import requests as req
import sys

from flask import Flask, request, redirect, url_for
from typing import Tuple
from wit import Wit

from . import keys as k


# URLs
GRAPH_API = 'https://graph.facebook.com/'
MESSENGER_PLATFORM = GRAPH_API+'v2.6/me/'
AUTH = 'access_token={token}&appsecret_proof={proof}'.format(
    token=k.FB_PAGE_ACCESS,
    proof=k.gen_app_secret_proof())
MESSAGES_URL = MESSENGER_PLATFORM+'messages?'+AUTH
    

def process_messages_event(req):
    """Handler for webhook (currently for postback and messages)"""

    try:  # parse JSON into data
        data = req.json()
    except Exception as e:
        return "Unable to parse JSON. Received error {}.".format(e)
    
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

            for m in entry['messaging']:
                try: 
                    fbId = m['sender']['id']
                except:
                    raise KeyError("Expected 'sender.id' in messaging") 

                turn_on_seen_and_typing_indicator(fbId)

                if 'text' in m['message'].keys():
                    handle_text(fbId, m['message']['text'])
                elif 'attachments' in m['message'].keys():
                    handle_attachment(fbId, m['message']['attachments'])
                else: 
                    return "Message body is empty."
    except Exception as e:
        return "Unexpected JSON structure. Received error: {}.".format(e)

    return 'OK'

def handle_attachment(fbId,str, attach):
    pass


def handle_text(fbId:str, text:str):
    response = Wit(access_token=k.WIT_TOK).message(
        msg=text, context={'session_id':fbId}, verbose=True)
    handle_message(response=response, fbId=fbId)


def fb_message(fbId:str, text:str):
    """
    Function for returning response to messenger
    """
    data = {
        'messaging_type': 'RESPONSE',
        'recipient': {'id': fbId},
        'message': {'text': text}
    }
    
    resp = req.post(MESSAGES_URL, json=data)


def first_entity_value(entities, entity):
    """
    Returns first entity value
    """
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def handle_message(response, fbId:str):
    """
    Customizes our response to the message and sends it
    """
    entities = response['entities']
    # Checks if user's message is a greeting
    # Otherwise we will just repeat what they sent us
    greetings = first_entity_value(entities, 'greetings')
    if greetings:
        text = "hello {{user_first_name}}!"
    else:
        text = "We've received your message: " + response['_text']
    # send message
    fb_message(fbId, text)


def turn_on_seen_and_typing_indicator(fbId):
    """POST to Messenger Platform to turn on sender actions"""
    data = {'messaging_type': 'RESPONSE', 
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


class greetings:
    @staticmethod
    def get():
        msgs = [
            'Greetings. Where are you headed?', 
            'Hello there. Where would you like to go?', 
            'Hello from the other sideee!', 
            'Sup! Where to?', 
            'Good day! Where are you off to?',
            ]
        return msgs[random.randint(0,len(msgs)-1)]






# TODO: for unsure traits, offer a "find nearest" button