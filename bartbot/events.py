# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
# from __future__ import unicode_literals

import json
import logging as log

import requests as req

from .processText import (handle_attachment, handle_text,
                          turn_on_seen_and_typing_indicator)
from .urls import MESSAGES_URL


def process_event(req) -> str:
    """Handler for webhook (currently for postback and messages)"""
    try:  # parse JSON into data
        data:dict = req.json
    except Exception as e:
        log.warning("Couldn't parse JSON with req.json.")
        return "Unable to parse JSON."
    log.info("Processed event JSON")
    log.debug("Processed event JSON: {}".format(
        json.dumps(data,indent=2)))

    res = "OK"
    try:  # switch for processing different request object types
        if data['object'] == 'page':
            log.info("Received 'page' object")
            if not 'entry' in data.keys():
                raise KeyError("Expected 'entry' in request object.")
            for entry in data['entry']:
                res = process_page_entry(entry)

        elif data['object'] == 'user':
            # TODO: Subscribed to name change. Implement change
            log.info("Received 'user' object")
            res = 'OK'

        else:
            raise KeyError(
                "Unexpected object, received {} object".format(
                    str(data['object'])))

    except KeyError as e:
        log.warning(
            "Couldn't parse JSON structure. Received error: {}.".format(e))
        res = "Unexpected JSON structure."

    except Exception as e:
        log.error("An unexpected error occurred. Error: {}.".format(e))
        res = "Not OK, but surviving. Check logs."

    return res


def process_page_entry(entry:dict) -> str:
    """Processes a page object returned by a message subscription"""
    if not 'messaging' in entry:
        raise KeyError("Expected 'messaging' in entry")

    for m in entry['messaging']:
        try: 
            fbId:str = m['sender']['id']
        except:
            raise KeyError("Expected 'sender.id' in messaging") 

        pre_response(fbId, m['message'])

        res:str = None
        if 'text' in m['message'].keys():
            log.info("Received text message event")
            res = handle_text(fbId, m['message']['text'])
        elif 'attachments' in m['message'].keys():
            log.info("Received attachment message event")
            res = handle_attachment(fbId, m['message']['attachments'])
        else: 
            log.warning("Received empty message event")
            res = "Message body is empty."
        
        res = post_response(res, fbId, m['message'])

        return res

def pre_response(fbId:str, messageObj:dict) -> None:
    """Tasks to prep for and set up response"""
    turn_on_seen_and_typing_indicator(fbId)

def post_response(result:str, fbId:str, messageObj:dict) -> str:
    """Tasks to clean up response before returning"""
    return result



# TODO: for unsure traits, offer a "find nearest" button
