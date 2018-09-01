from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import hashlib
import hmac
import json
import os
import random
import requests as req

from flask import Flask, request, redirect, url_for
from wit import Wit

from . import challenge

app = Flask(__name__)

# Environment variables
FB_PAGE_ACCESS = os.environ.get('FB_PAGE_ACCESS')
FB_PAGE_ACCESS_2 = os.environ.get('FB_PAGE_ACCESS_2')
FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')
WIT_TOKEN = os.environ.get('WIT_TOKEN')

# URLs
GRAPH_API = 'https://graph.facebook.com/'
MESSENGER_PLATFORM = GRAPH_API+'v2.6/me/'
MESSAGES_URL = MESSENGER_PLATFORM+'messages?'+gen_auth_queries()


def get_random_int(lower_bound=1, upper_bound=10):
    return random.randomint(lower_bound, upper_bound)


def gen_auth_queries():
    """Calculates AUTH from SHA256"""
    return 'access_token={token}&appsecret_proof={proof}'.format(
        token=FB_PAGE_ACCESS,
        proof=hmac.new(
            FB_PAGE_ACCESS_2.encode('utf-8'),
            msg=FB_PAGE_ACCESS.encode('utf-8'),
            digestmod=hashlib.sha256)
                .hexdigest())


@app.route("/")
def main_handle():
    # print("in main handle")
    # return redirect(url_for('webhook'))
    return "Hello! This is the main API endpoint for Bartbot. What is Bartbot you ask? Check out <a href=\"http://github.com/anwyho/bartbot\">github.com/anwyho/bartbot</a> for more details."


@app.route("/webhook", methods=['POST', 'GET'])
def handle_webhook():
    # TODO: Verify SHA-1
    if request.method == 'GET':
        return challenge.process_get(request)
    elif request.method == 'POST':
        return process_messages_event(request)
    else:
        return "Unsupported HTTPS Verb."





def process_messages_event(request):
    """
    Handler for webhook (currently for postback and messages)
    """
    try:
        data = request.json
    except Exception as e:
        return "Unable to parse json. Received error {}.".format(e)

    try:
        if data['object'] == 'page':
            for entry in data['entry']:
                messaging = entry['messaging']
                if len(ms) > 0 and messaging[0]:
                    m = messaging[0]
                    fb_id = m['sender']['id']

                    if 'text' in m['message'].keys():
                        handle_text(m['message']['text'])
                    elif 'attachments' in m['message'].keys():
                        handle_attachment(m['message']['attachments'])
                    
                    turn_on_seen_and_typing_indicator(fb_id)

    except Exception as e:
        return "Unable to decipher json. Received error {}.".format(e)

    return 'OK'


def handle_text(text):
    response = Wit(access_token=WIT_TOKEN).message(
        msg=text, context={'session_id':fb_id}, verbose=True)
    handle_message(response=response, fb_id=fb_id)


def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {
        'messaging_type': 'RESPONSE',
        'recipient': {'id': sender_id},
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


def handle_message(response, fb_id):
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
    fb_message(fb_id, text)

def turn_on_seen_and_typing_indicator(fb_id):
    data = {
        'messaging_type': 'RESPONSE', 
        'recipient': { 'id': fb_id }
    }

    data['sender_action'] = 'mark_seen'
    resp = req.post(MESSAGES_URL, json=data)
    data['sender_action'] = 'typing_on'
    resp = req.post(MESSAGES_URL, json=data)
    


def get_id_name(fb_id):
    data = {'fields':['first_name','last_name']}
    resp = req.get(GRAPH_API+AUTH+fb_id+'?', json=data)
    if "error" in resp.keys():
        return None
    else: return resp['first_name'], resp['last_name']





if __name__ == '__main__':
    app.run()
