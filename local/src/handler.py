from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import requests
import json
from sys import argv
from flask import Flask, request, redirect, url_for
# from wit import Wit

app = Flask(__name__)

# WIT_TOKEN = os.environ.get('WIT_TOKEN')
FB_PAGE_TOKEN = os.environ.get('FB_PAGE_TOKEN')
FB_VERIFY_TOKEN = os.environ.get('FB_VERIFY_TOKEN')

FB_PAGE_ACCESS_TOKEN = "EAADFvGcu0k4BAEDPXrULwvkFDP6tqmwLTOJJPah6GO9OEndFggkXMosHmRzO4edZAZCtEuFv6TvcLDDQvr6eMeb2XDZAZBLKoZAOIZAVPzgsQcn96AZCj10Ek653lsiUerZCqlchqqtZBxLh1S71XmYdAr7vsgEGvxCUpbyBiGzUrYAZDZD"
FB_VERIFY_TOKEN = "OF_MY_APPRECIATION"
# WIT_TOKEN = "SS3OBO2R4BNYYUBW6EBI4WR2ZJO4VIF3"

@app.route("/")
def main_handle():
    # print("in main handle")
    # return redirect(url_for('webhook'))
    return "In main handle"


@app.route("/webhook", methods=['POST', 'GET'])
def handle_webhook():
    if request.method == 'GET':
        return webhook_challenge(request)
    elif request.method == 'POST':
        # return simple_post(request)
        return messenger_post(request)
    else:
        return "Unsupported HTTPS Verb."


# def simple_post(request):
#     data = request.args
#     if data['object'] == 'page':
#         req = requests.post()


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
        return 'Invalid Request or Verification Token'


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
                if fb_id != '<PSID>':
                    raise ValueError("fb_id: {}".format(fb_id))
                # We retrieve the message content
                text = message['message']['text']

                fb_message(fb_id,text)

                # # Let's forward the message to Wit /message
                # # and customize our response to the message in handle_message
                # response = Wit(access_token=WIT_TOKEN).message(msg=text, context={'session_id':fb_id}, verbose=True)
                # handle_message(response=response, fb_id=fb_id)
    else:
        # Returned another event
        return 'Received Different Event'
    return Non


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
    qs = 'access_token=' + FB_PAGE_TOKEN
    # Send POST request to messenger
    resp = requests.post('https://graph.facebook.com/v2.6/me/messages?' + qs,
                         json=data)
    return resp.content


# def first_entity_value(entities, entity):
#     """
#     Returns first entity value
#     """
#     if entity not in entities:
#         return None
#     val = entities[entity][0]['value']
#     if not val:
#         return None
#     return val['value'] if isinstance(val, dict) else val


# def handle_message(response, fb_id):
#     """
#     Customizes our response to the message and sends it
#     """
#     entities = response['entities']
#     # Checks if user's message is a greeting
#     # Otherwise we will just repeat what they sent us
#     greetings = first_entity_value(entities, 'greetings')
#     if greetings:
#         text = "hello!"
#     else:
#         text = "We've received your message: " + response['_text']
#     # send message
#     fb_message(fb_id, text)


if __name__ == '__main__':
    app.run()