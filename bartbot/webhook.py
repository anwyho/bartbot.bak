# from __future__ import absolute_import
# from __future__ import print_function

# TODO: File-level docstrings 


import logging
import os
# TODO: Look into logging that filters out sensitive info

from flask import (Flask, request)

from .events.event import process_event
from .challenge import verify_challenge

app = Flask(__name__)

DEBUG = True


@app.route("/")
def main_handle():
    """Returns static website for Bartbot info"""
    # TODO turn this into staticly delivered website
    return """Hello! This is the main API endpoint for Bartbot. What is Bartbot you ask? Check out <a href=\"http://github.com/anwyho/bartbot\">github.com/anwyho/bartbot</a> for more details."""


@app.route("/webhook", methods=['POST', 'GET'])
def handle_webhook():
    """Processes POST and GET requests from the Messenger Platform"""

    # Set up logging configuration
    logFile = os.path.join( '.',
        'bartbot',
        '.logs', 
        '.bartbot-{}.log'.format('debug' if DEBUG else 'info'))
    os.makedirs(os.path.dirname(logFile), exist_ok=True)
    logFormat = "%(levelname)s:%(module)s:%(lineno)d %(message)s:%(asctime)s"

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        filename=logFile, 
        format=logFormat, 
        level=logging.DEBUG if DEBUG else logging.INFO)

    logging.info("S T A R T I N G   L O G")

    res = None
    if verify_request(request):
        res = process_request(request)
    else:
        res = "Invalid request. Failed SHA-1 verification."

    logging.info("E N D I N G   L O G")
    logging.shutdown()

    return res+'\n'


def process_request(request) -> str:
    """
    Passes request onto other methods depending on request method
    """
    
    if request.method == 'GET':
        res = verify_challenge(request)
    elif request.method == 'POST':
        res = process_event(request)
    else:
        res = "Unsupported HTTPS Verb."
        
    return res


def verify_request(request) -> bool:
    """Verifies SHA-1 of entire message"""
    # TODO: Verify SHA-1
    return True

    

if __name__ == '__main__':
    app.run()
