from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

import os
import requests
import json
from sys import argv
from flask import Flask, request
from wit import Wit

app = Flask(__name__)

# xray_recorder.configure(service='handler')
# XRayMiddleware(app, xray_recorder)


# Wit.ai parameters
WIT_TOKEN = os.environ.get('WIT_TOKEN')
# WIT_TOKEN = 'SS3OBO2R4BNYYUBW6EBI4WR2ZJO4VIF3'
# Messenger API parameters
FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN')
# FB_PAGE_TOKEN = 'EAADFvGcu0k4BAA76OyWLPxlGxOZAJCsNgGFbfZBXYZBp3olboQoZAJfCJMUZBwUGiannE8oS62q2jXlnM9DGNhIwnP8bQYPhbPsjFylPtMYAiOvK4YsgVxzhOQBnhbHDjWC1MwSOqS0iO5NpJSWNNJ2XuKJ88xz6C4xZAQBXEM13smZBuijWHLd'
# A user secret to verify webhook get request.
FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')
# FB_VERIFY_TOKEN = 'OF_MY_APPRECIATION'


@app.route("/")
def main_handle():
    return "in main handle"

@app.route("/webhook", methods=['POST', 'GET'])
def handle_webhook():
    if request.method == 'GET':
        webhook_challenge()

    """
    A webhook to return a challenge
    """
    if request.method == 'GET':
        query = request.args
        verify_token = query['hub.verify_token']
        # check whether the verify tokens match
        if query['hub.mode'] == 'subscribe' and \
                verify_token == FB_VERIFY_TOKEN:
            # respond with the challenge to confirm
            challenge = query['hub.challenge']
            return challenge
        else:
            return 'Invalid Request or Verification Token'
    else:
        return messenger_post()

def messenger_post():
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
                # We retrieve the message content
                text = message['message']['text']
                # Let's forward the message to Wit /message
                # and customize our response to the message in handle_message
                response = client.message(msg=text, context={'session_id':fb_id})
                handle_message(response=response, fb_id=fb_id)
    else:
        # Returned another event
        return 'Received Different Event'
    return None

def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }
    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + FB_PAGE_TOKEN
    # Send POST request to messenger
    resp = requests.post('https://graph.facebook.com/me/messages?' + qs,
                         json=data)
    return resp.content


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

# Setup Wit Client
client = Wit(access_token=WIT_TOKEN)

if __name__ == '__main__':
    app.run()