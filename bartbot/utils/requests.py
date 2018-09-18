"""
Provides requests package wrapper to facilitate logging and error handling. Helps aleviate code duplication.
"""

import json
import logging
import requests

from typing import Tuple

from .errors import handle_request_error


def post(*args, **kwargs) -> Tuple[bool,dict]:
    """
    Sends POST request to given URL with error handling.
    Returns OK and response as a dict.
    """

    logging.info("Performing POST request") 
    if 'json' in kwargs:
        logging.debug(f"POSTing to URL {args[0] if len(args) else kwargs['url']} \nwith data {json.dumps(kwargs['json'],indent=2)}")
    resp = requests.post(*args, **kwargs).json()
    ok:bool = handle_request_error(resp)
    return ok, resp


def get(*args, **kwargs) -> Tuple[bool,dict]:
    """
    Sends GET request to given URL with error handling.
    Returns OK and response as a dict.
    """

    logging.info("Performing GET request") 
    if 'json' in kwargs:
        logging.debug(f"GETing to URL {args[0] if len(args) else kwargs['url']} \nwith queries {json.dumps(kwargs['json'],indent=2)}")
    resp = requests.get(*args, **kwargs).json()
    ok:bool = handle_request_error(resp)
    return ok, resp


