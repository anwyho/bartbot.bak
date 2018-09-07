# TODO: File-level docstrings


import logging  # TODO: Look into logging that filters out sensitive info
import os

from flask import (Flask, request)

from .events.event import process_event
from .utils.keys import FB_VERIFY_TOK


app = Flask(__name__)

DEBUG = True


@app.route("/")
def main_handle():
    """Returns static website for Bartbot info"""
    # TODO turn this into staticly delivered website
    logging.info("In main handle")
    return """Hello! This is the main API endpoint for Bartbot. What is Bartbot you ask? Check out <a href=\"http://github.com/anwyho/bartbot\">github.com/anwyho/bartbot</a> for more details."""


@app.route("/webhook", methods=['POST', 'GET'])
def handle_webhook():
    """Processes POST and GET requests from the Messenger Platform"""


    # try:
    #     # Set up logging configuration
    #     logFile = os.path.join( '.',
    #         'bartbot',
    #         '.logs', 
    #         '.bartbot-{}.log'.format('debug' if DEBUG else 'info'))
    #     os.makedirs(os.path.dirname(logFile), exist_ok=True)
    # except Exception as e:
    #     logFile.error(f"Couldn't make log file {logFile}. Error: {e}")

    # logFormat = \
    #         "%(levelname)s:%(module)s:%(lineno)d %(message)s:%(asctime)s"

    # try:
    #     # TODO: Check if uncommenting this breaks AWS Lambda
    #     for handler in logging.root.handlers[:]:
    #         print(handler)
    #         logging.root.removeHandler(handler)

    #     logging.basicConfig(
    #         filename=logFile, 
    #     # logging.basicConfig(
    #         format=logFormat, 
    #         level=logging.DEBUG if DEBUG else logging.INFO)
    # except Exception as e:
    #     logFile.error(f"Couldn't configure logfile. Error: {e}")




    logging.info("\n\nS T A R T I N G   N E W   L O G\n\n")

    if verify_request(request):
        res = process_request(request)
    else:
        res = "Invalid request. Failed SHA-1 verification."

    logging.info("E N D I N G   L O G")
    logging.shutdown()

    return res+'\n'


def verify_request(request) -> bool:
    """Verifies SHA-1 of message"""
    # TODO: Verify SHA-1
    return True


def process_request(request) -> str:
    """
    Passes request onto other methods depending on request method
    """

    res = None 
    if request.method == 'GET':
        res = verify_challenge(request)
    elif request.method == 'POST':
        res = process_event(request)
    else:
        res = "Unsupported HTTPS Verb."
        
    return res


def verify_challenge(req):
    """
    Verifies and fulfills Messenger Platform GET challenge
    """

    logging.info('Verifying challenge')

    qParams = req.args
    if 'hub.verify_token' in qParams.keys() and \
        'hub.mode' in qParams.keys() and \
        'hub.challenge' in qParams.keys():

        if qParams['hub.verify_token'] == FB_VERIFY_TOK and \
                qParams['hub.mode'] == 'subscribe':
            logging.info("Verified token.")
            return qParams['hub.challenge']
        else: 
            logging.info("Unable to verify token. Either " + \
                f"{qParams['hub.verify_token']} != {FB_VERIFY_TOK} " + \
                f"or {qParams['hub.mode']} != 'subscribe'")
            return 'Invalid request or verification token.'
    else: 
        logging.info("GET did not include all necessary parameters")
        return 'Invalid request or verification token.'



if __name__ == '__main__':
    app.run()




# TODO: This should be in a unittest module

   # try:
    #     # Set up logging configuration
    #     logFile = os.path.join( '.',
    #         'bartbot',
    #         '.logs', 
    #         '.bartbot-{}.log'.format('debug' if DEBUG else 'info'))
    #     os.makedirs(os.path.dirname(logFile), exist_ok=True)
    # except Exception as e:
    #     logFile.error(f"Couldn't make log file {logFile}. Error: {e}")

    #     logFormat = \
    #         "%(levelname)s:%(module)s:%(lineno)d %(message)s:%(asctime)s"

    # try:
    #     # TODO: Check if uncommenting this breaks AWS Lambda
    #     for handler in logging.root.handlers[:]:
    #         print(handler)
    #         logging.root.removeHandler(handler)
    #     logging.basicConfig(
    #         filename=logFile, 
    #     # logging.basicConfig(
    #         format=logFormat, 
    #         level=logging.DEBUG if DEBUG else logging.INFO)
    # except Exception as e:
    #     logFile.error(f"Couldn't configure logfile. Error: {e}")