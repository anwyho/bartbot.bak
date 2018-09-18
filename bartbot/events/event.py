import json
import logging

from flask import request

from .pages.page import process_page_entry


def process_event(req:request) -> str:
    """
    Handler for webhook (currently only for postback, referrals, and messages)
    """
    try:  # parse JSON into data
        data:dict = req.json
    except Exception as e:
        logging.warning(f"Couldn't parse JSON with req.json. Error: {e}")
        res = "Unable to parse JSON."
    else: 
        logging.debug(f"Processed event JSON: {json.dumps(data,indent=2)}")
        res = identify_object(data)
    finally:
        return res


def identify_object(data:dict) -> str:
    if data['object'] == 'page':
        logging.info("Received 'page' object")
        if 'entry' in data.keys():
            res = ""
            for entry in data['entry']:
                res += f"{process_page_entry(entry)}\n"
        else:
            logging.warning(
                f"Object doesn't have the right structure. Error: {e}.")
            res = "Unexpected JSON structure."

    elif data['object'] == 'user':
        logging.info("Received 'user' object")
        # TODO: Subscribed to name  change. Implement change
        # NOTE: Is this even necessary? We query FB for names every time
            # and don't have a database to store the names in...
        res = 'OK'
        
    else:
        res = f"Unexpected object; received {str(data['object'])} object"

    return res