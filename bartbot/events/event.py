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
        logging.warning("Couldn't parse JSON with req.json.")
        return "Unable to parse JSON."
    logging.info("Processed event JSON")
    logging.debug(f"Processed event JSON: {json.dumps(data,indent=2)}")

    res = None
    try:  # switch for processing different request object types
        if data['object'] == 'page':
            logging.info("Received 'page' object")
            if not 'entry' in data.keys():
                raise ValueError("Expected 'entry' in request object.")
            for entry in data['entry']:
                res = process_page_entry(entry)

        elif data['object'] == 'user':
            # NOTE: Is this even necessary? We query FB for names every time
                # and don't have a database to store the names in
            logging.info("Received 'user' object")
            # TODO: Subscribed to name change. Implement change
            
            res = 'OK'

        else:
            raise ValueError(
                "Unexpected object, received {str(data['object'])} object")
    
    except ValueError as e:
        logging.warning(
            f"Object doesn't have the right structure. Error: {e}.")
        res = "Unexpected JSON structure."

    except Exception as e:
        logging.error(f"An unexpected error occurred. Error: {e}.")
        res = "Not OK, but surviving. Check logs."

    return res
