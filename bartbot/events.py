# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function
# from __future__ import unicode_literals

import json
import logging as log

import requests as req

from .processPage import process_page_entry
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
