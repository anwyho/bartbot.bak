# TODO: File-level docstrings

import json
# TODO: Look into logging that filters out sensitive info
import logging
import os
import sys
import traceback

from flask import (Flask, request)

from bartbot.receive.event import (process_event)
from bartbot.utils.keys import (verify_challenge, verify_signature)


app = Flask(__name__)

bartbotGithubHtml: str = \
    '<a href="http://github.com/anwyho/bartbot">github.com/anwyho/bartbot</a>'
APP_HANDLE_TEXT: str = f'Hello! This is the main API endpoint for Bartbot. What is Bartbot you ask? Check out {bartbotGithubHtml} for more details.'


@app.route("/")
def main_handle() -> str:
    """Returns static website for Bartbot info"""
    # TODO turn this into staticly delivered website
    logging.info("In main handle")
    global APP_HANDLE_TEXT
    return APP_HANDLE_TEXT


# # TODO: Figure out if Rollbar is right for this project
# import rollbar
# rollbar.init( '98567a2c950c430381b1750e022bf60d', environment='development')
# @rollbar.lambda_function
    # rollbar.report_message('Hello from Lambda', 'info')
    # raise NotImplementedError("Test the rollbar")

@app.route("/webhook", methods=['POST', 'GET'])
def handle_webhook() -> str:
    """
    Processes POST and GET requests from the Messenger Platform
    """
    # respMsg = ""
    # respMsg += str(process_event(request))
    # return respMsg

    respMsg: str = ""
    try:
        if verify_signature(request):
            if request.method == 'GET':
                respMsg += verify_challenge(request.args, respMsg)[1]
            elif request.method == 'POST':
                results = process_event(request)
                for event in results:
                    for message in event:
                        messageResult = f"\n{'Sent!' if message[0] else 'FAILURE'} - {message[1]}"
                        if len(messageResult) > 60:
                            messageResult = messageResult[:57] + "..."
                        respMsg += messageResult
            else:
                respMsg += "Unsupported HTTPS Verb.\n"
        else:
            respMsg += "Invalid request. Failed SHA-1 verification.\n"

    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        traceback.print_tb(exc_tb)
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logging.debug(
            f"An unexpected error occurred. Error: {e}. Error info: "
            f"{exc_type}, {fname}, {exc_tb.tb_lineno}")
        respMsg += f"An unexpected error occurred. Error: {e}. Error "
        f"info: {exc_type}, {fname}, {exc_tb.tb_lineno}"
        respMsg += "\nERROR: Not OK, but surviving. Check logs\n"

    finally:
        return str(respMsg) + "\nDone!\n"


@app.route("/debug", methods=['GET'])
def debug() -> str:
    # TODO: Logging in this function
    # TODO: Connect keyword GET query parsing with keyword message parsing
    qParams = request.args
    print(qParams)

    from .utils.keys import DEBUG_TOK
    if 'debug_tok' in qParams and qParams['debug_tok'] == DEBUG_TOK:

        if 'scripts' in qParams:
            from .scripts import setMessengerProfile as prof

            res = json.dumps(prof.run_scripts(
                qParams['scripts']), indent=2)
            return f"Ran scripts with results {res}."
    return "OK"


if __name__ == '__main__':
    from .utils.keys import FLASK_ENV
    app.run(debug=(FLASK_ENV == 'development'))


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
    # DEBUG = True
