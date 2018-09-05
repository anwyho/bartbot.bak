import logging

from ...utils.requests import post
from ...utils.urls import MESSAGES_API
from .message import handle_message
from .postback import handle_postback


def process_page_entry(entry:dict) -> str:
    """Processes a page object returned by a message subscription"""
    
    if not 'messaging' in entry:
        raise KeyError("Expected 'messaging' in entry")

    for message in entry['messaging']:
        try: 
            fbId:str = message['sender']['id']
        except KeyError as e:
            raise KeyError("Expected 'sender.id' in messaging. " + \
                f"Received error: {e}.") 

        turn_on_seen_and_typing_indicator(fbId)

        res = None
        if 'message' in message.keys():
            logging.info("Received message")
            res = handle_message(fbId, message['message'])

        elif 'postback' in message.keys():
            logging.info("Received postback")
            res = handle_postback(fbId, message['postback'])

        else: 
            res = "Unsupported subsription. Only supporting 'messages', 'messaging_postbacks', and 'messaging referrals'."

        return res

        
def turn_on_seen_and_typing_indicator(fbId:str):
    """POST to Messenger Platform to turn on sender actions"""
    data = {
        'messaging_type': 'RESPONSE', 
        'recipient': { 'id': fbId }}

    data['sender_action'] = 'mark_seen'
    ok, _ = post(MESSAGES_API, json=data)
    if ok:
        data['sender_action'] = 'typing_on'
        ok, _ = post(MESSAGES_API, json=data)
        if not ok: 
            logging.error("Didn't complete 'typing_on' sender action.")
    else: 
        logging.error("Didn't complete 'mark_seen' sender action.")






# def first_entity_value(entities, entity):
#     """Returns first entity value"""
#     if entity not in entities:
#         return None
#     val = entities[entity][0]['value']
#     if not val:
#         return None
#     return val['value'] if isinstance(val, dict) else val

# def pre_response(fbId:str, messageObj:dict) -> None:
#     """Tasks to prep for and set up response"""
#     turn_on_seen_and_typing_indicator(fbId)    

# def post_response(result:str, fbId:str, messageObj:dict) -> str:
#     """Tasks to clean up response before returning"""
#     return result