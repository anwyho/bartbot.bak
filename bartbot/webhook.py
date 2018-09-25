# TODO: File-level docstrings

import json
# TODO: Look into logging that filters out sensitive info
import logging  
import os
import sys
import traceback

from flask import (Flask, request)

from .events.event import process_event
from .utils.keys import (verify_challenge, verify_signature)


app = Flask(__name__)

DEBUG = True


@app.route("/")
def main_handle():
    """Returns static website for Bartbot info"""
    # TODO turn this into staticly delivered website
    logging.info("In main handle")
    return """Hello! This is the main API endpoint for Bartbot. What is Bartbot you ask? Check out <a href=\"http://github.com/anwyho/bartbot\">github.com/anwyho/bartbot</a> for more details."""


# # TODO: Figure out if Rollbar is right for this project
# import rollbar
# rollbar.init( '98567a2c950c430381b1750e022bf60d', environment='development')
# @rollbar.lambda_function

@app.route("/webhook", methods=['POST', 'GET'])
def handle_webhook() -> str:
    """Processes POST and GET requests from the Messenger Platform"""
    # rollbar.report_message('Hello from Lambda', 'info')
    # raise NotImplementedError("Test the rollbar")


    respMsg:str = ""
    try: 
        if verify_signature(request): 
            respMsg += process_request(request, respMsg)
        else: 
            respMsg += "Invalid request. Failed SHA-1 verification.\n"

    except Exception as e:

        exc_type, _, exc_tb = sys.exc_info()
        traceback.print_tb(exc_tb)
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        logging.debug(f"An unexpected error occurred. Error: {e}. Error info: {exc_type}, {fname}, {exc_tb.tb_lineno}")
        respMsg += f"An unexpected error occurred. Error: {e}. Error info: {exc_type}, {fname}, {exc_tb.tb_lineno}"

        respMsg += "\nERROR: Not OK, but surviving. Check logs\n"
    
    finally:
        return respMsg


def process_request(request, respMsg:str) -> str:
    """
    Passes request onto other methods depending on request method
    """

    if request.method == 'GET':
        respMsg += verify_challenge(request, respMsg)
    elif request.method == 'POST':
        respMsg += process_event(request, respMsg)
    else:
        respMsg += "Unsupported HTTPS Verb.\n"
    
    return respMsg


@app.route("/debug", methods=['GET'])
def debug():
    # TODO: Logging in this function
    # TODO: Connect keyword GET query parsing with keyword message parsing
    qParams = request.args
    print(qParams)

    from .utils.keys import DEBUG_TOK 
    if 'debug_tok' in qParams and qParams['debug_tok'] == DEBUG_TOK:
        
        if 'scripts' in qParams:
            from .scripts import setMessengerProfile as prof
            
            respMsg = json.dumps(prof.run_scripts(qParams['scripts']), indent=2)
            return f"Ran scripts with results {res}."
    return "OK"


if __name__ == '__main__':
    app.run()



# TODO: Check out how pywit handles logging in __init__.py


    # # TODO: This should be in a unittest module
    # try:
    #     # Set up logging configuration
    #     logFile = os.path.join( '.',
    #         'bartbot',
    #         '.logs', 
    #         '.bartbot-{}.log'.format('debug' if DEBUG else 'info'))
    #     os.makedirs(os.path.dirname(logFile), exist_ok=True)
    # except Exception as e:
    #     logging.error(f"Couldn't make log file {logFile}. Error: {e}")

    # logFormat = \
    #     "%(levelname)s:%(module)s:%(lineno)d %(message)s:%(asctime)s"

    # try:
    #     # # TODO: Check if uncommenting this breaks AWS Lambda
    #     # for handler in logging.root.handlers[:]:
    #     #     print(handler)
            
    #     logging.basicConfig(
    #         filename=logFile, 
    #         format=logFormat, 
    #         level=logging.DEBUG if DEBUG else logging.INFO)
    # except Exception as e:
    #     logging.error(f"Couldn't configure logfile. Error: {e}")

    # logging.info("\n\nS T A R T I N G   N E W   L O G\n\n")


    # # The above is a mess of logging.


        #     logging.info("E N D I N G   L O G")
        # logging.shutdown()