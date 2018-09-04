import json
import logging
import requests

from typing import Tuple

from .errors import handle_request_error
from .urls import MESSAGES_API


def post(*args, **kwargs) -> Tuple[bool,dict]:
    """
    Sends POST request to given URL with error handling.
    Returns OK and response as a dict.
    """

    logging.info("Performing POST request") 
    if 'json' in kwargs:
        logging.debug("POSTing to URL {} \nwith data {}".format(
            args[0],json.dumps(kwargs['json'],indent=2)))
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
        logging.debug("GETing to URL {} \nwith queries {}".format(
            args[0],json.dumps(kwargs['json'],indent=2)))
    resp = requests.get(*args, **kwargs).json()
    ok:bool = handle_request_error(resp)
    return ok, resp


