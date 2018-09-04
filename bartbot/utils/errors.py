
import logging
import json

def handle_request_error(response:dict) -> bool:
    """
    Returns True if no error and False if error. 
    Handles error and outputs to logs.
    """

    logging.debug("Response: {}".format(json.dumps(response))) 

    if 'error' in response: 
        # TODO: More apecific responses
        return False
    else:
        return True