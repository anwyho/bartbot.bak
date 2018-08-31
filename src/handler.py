from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import hashlib
import hmac
import json
import os
import requests

from flask import Flask, request, redirect, url_for
from wit import Wit

app = Flask(__name__)

FB_PAGE_ACCESS = os.environ.get('FB_PAGE_ACCESS')
FB_PAGE_ACCESS_2 = os.environ.get('FB_PAGE_ACCESS_2')
FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')
WIT_TOKEN = os.environ.get('WIT_TOKEN')
FB_MESSAGES_URL = 'https://graph.facebook.com/v2.6/me/messages?'

@app.route("/")
def main_handle():
    # print("in main handle")
    # return redirect(url_for('webhook'))
    return "Hello! This is the main API endpoint for Bartbot. What is Bartbot you ask? Check out <a href=\"http://github.com/anwyho/bartbot\">github.com/anwyho/bartbot</a> for more details."


@app.route("/webhook", methods=['POST', 'GET'])
def handle_webhook():

    # TODO: Verify SHA-1

    if request.method == 'GET':
        return webhook_challenge(request)
    elif request.method == 'POST':
        # return simple_post(request)
        return messenger_post(request)
    else:
        return "Unsupported HTTPS Verb."


def webhook_challenge(request):
    """
    A webhook to return a challenge
    """
    queryParams = request.args
    verify_token = queryParams['hub.verify_token']
    # check whether the verify tokens match
    if queryParams['hub.mode'] == 'subscribe' and \
            verify_token == FB_VERIFY_TOKEN:
        # respond with the challenge to confirm
        challenge = queryParams['hub.challenge']
        return challenge
    else:
        return 'Invalid Request or Verification Token. Expected FB_PAGE_ACCESS={} and FB_VERIFY_TOKEN={}'.format(FB_PAGE_ACCESS,FB_VERIFY_TOKEN)


def messenger_post(request):
    """
    Handler for webhook (currently for postback and messages)
    """

    data = request.json
    if data['object'] == 'page':
        for entry in data['entry']:
            # get all the messages
            messages = entry['messaging']
            if messages[0]:
                # Get the first message
                message = messages[0]
                # Yay! We got a new message!
                # We retrieve the Facebook user ID of the sender
                fb_id = message['sender']['id']
                if fb_id == '<PSID>':
                    raise ValueError("Invalid FB user ID: {}".format(fb_id))
                # We retrieve the message content
                text = message['message']['text']

                turn_on_seen_and_typing_indicator(fb_id)

                # Let's forward the message to Wit /message
                # and customize our response to the message in handle_message
                response = Wit(access_token=WIT_TOKEN).message(msg=text, context={'session_id':fb_id}, verbose=True)
                handle_message(response=response, fb_id=fb_id)
    else:
        # Returned another event
        return 'Received Different Event'
    return 'OK'

def app_secret_proof():
    return hmac.new(FB_PAGE_ACCESS_2.encode('utf-8'),msg=FB_PAGE_ACCESS.encode('utf-8'),digestmod=hashlib.sha256).hexdigest()


def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {
        'messaging_type': 'RESPONSE',
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }

    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + FB_PAGE_ACCESS + \
        '&appsecret+proof=' + app_secret_proof() 
    # Send POST request to messenger
    resp = requests.post(FB_MESSAGES_URL + qs,
                         json=data)


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
        text = "hello!"
    else:
        text = "We've received your message: " + response['_text']
    # send message
    fb_message(fb_id, text)

def turn_on_seen_and_typing_indicator(fb_id):
    data = {
        'messaging_type': 'RESPONSE', 
        'recipient': { 'id': fb_id }
    }

    qs = 'access_token=' + FB_PAGE_ACCESS + \
        '&appsecret+proof=' + app_secret_proof() 

    data['sender_action'] = 'typing_on'
    resp = requests.post(FB_MESSAGES_URL+qs, json=data)
    data['sender_action'] = 'mark_seen'
    resp = requests.post(FB_MESSAGES_URL+qs, json=data)


if __name__ == '__main__':
    app.run()