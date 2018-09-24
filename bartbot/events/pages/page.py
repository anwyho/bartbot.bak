import logging

from ...utils.requests import post
from ...utils.urls import MESSAGES_API
from .messages.message import handle_message
from .postbacks.postback import handle_postback
from .referrals.referral import handle_referral


def process_page_entry(entry:dict, respMsg:str) -> str:
    """Processes a page object returned by a message subscription"""
    
    if not 'messaging' in entry:
        respMsg += "Unexpected JSON structure. Expected 'messaging' in entry object.\n"
    
    else: 
        for message in entry['messaging']:
            try: 
                fbId:str = message['sender']['id']
            except KeyError as e:
                respMsg += f"Unexpected JSON structure. Expected 'sender.id' in messaging. Received error: {e}.\n"
            else:
                respMsg += "Typing ON success: {}\n".format(
                    toggle_seen_and_typing_indicator(fbId, True))
                respMsg = identify_message(fbId, message, respMsg)
                respMsg += "Typing OFF success: {}\n".format(
                    toggle_seen_and_typing_indicator(fbId, False))
    return respMsg

def identify_message(fbId:str, message:str, respMsg:str) -> str: 
    if 'message' in message.keys():
        logging.info("Received message")
        respMsg += handle_message(fbId, message['message'], respMsg)

    elif 'postback' in message.keys():
        logging.info("Received postback")
        respMsg += handle_postback(fbId, message['postback'], respMsg)

    elif 'referral' in message.keys():
        logging.info("Received referral")
        respMsg += handle_referral(fbId, message['referral'], respMsg)
            
    else: 
        respMsg = "Unsupported subsription. Only supporting 'messages', 'messaging_postbacks', and 'messaging_referrals'.\n"

    return respMsg


# TODO: Bundle these two requests into a batch request
# https://developers.facebook.com/docs/graph-api/making-multiple-requests
# curl -F 'access_token=...&batch=[{"method":"GET", "relative_url":"me"},{"method":"GET", "relative_url":"me/friends?limit=50"}]' https://graph.facebook.com
# data = {
#     'batch' : [data]
# }
def toggle_seen_and_typing_indicator(fbId:str, on:bool) -> None:
    """POST to Messenger Platform to turn on sender actions"""
    data = {
        'messaging_type': 'RESPONSE', 
        'recipient': { 'id': fbId }}

    if on:
        data['sender_action'] = 'mark_seen'
        isOk = post(MESSAGES_API, json=data)[0]
        data['sender_action'] = 'typing_on'
        isOk = post(MESSAGES_API, json=data)[0] and isOk
        if not isOk: 
            logging.warning("Didn't complete 'typing_on' and/or 'mark_seen' sender action.")
    else: 
        data['sender_action'] = 'typing_off'
        isOk = post(MESSAGES_API, json=data)[0]
        if not isOk: 
            logging.warning("Didn't complete 'typing_off' sender action.")
    return isOk


# NOTE: I can possibly use these later
# def pre_response(fbId:str, messageObj:dict) -> None:
#     """Tasks to prep for and set up response"""
#     turn_on_seen_and_typing_indicator(fbId)    

# def post_response(result:str, fbId:str, messageObj:dict) -> str:
#     """Tasks to clean up response before returning"""
#     return result