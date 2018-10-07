import json
import logging

from flask import request
from typing import (List, Optional, Tuple, Type, Union)

from bartbot.messages import (Attachment, Message, Postback, Referral, Text)
from bartbot.events.pages.page import process_page_entry


def process_event(req: request, respMsg: str) -> str:
    """
    Handler for webhook (currently only for postback, referrals, and messages)
    """
    try:  # parse flak request JSON into data dict
        data: dict = req.json

    except Exception as e:
        logging.warning(f"Couldn't parse JSON with req.json. Error: {e}")
        respMsg += "Unable to parse JSON.\n"

    else:
        logging.debug(f"Processed event JSON: {json.dumps(data,indent=2)}")
        respMsg += identify_object(data, respMsg)

    finally:
        return respMsg


def identify_object(data: dict, respMsg: str) -> str:
    if data['object'] == 'page':
        logging.info("Received 'page' object")
        if 'entry' in data.keys():
            for entry in data['entry']:
                respMsg += process_page_entry(entry, respMsg)

        else:
            # logging.warning(
            #     f"Object doesn't have the right structure. Error: {e}.")
            respMsg += "Unexpected JSON structure. Expected 'entry' in page object.\n"

    elif data['object'] == 'user':
        logging.info("Received 'user' object")
        # TODO: Subscribed to name  change. Implement change
        # NOTE: Is this even necessary? We query FB for names every time
        # and don't have a database to store the names in...
        respMsg += "Received 'user' object. Response not implemented yet.\n"

    else:
        respMsg += f"Unexpected object; received {str(data['object'])} object\n"

    return respMsg
