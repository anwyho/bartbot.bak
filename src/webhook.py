# from __future__ import absolute_import
# from __future__ import print_function

import logging as log
import sys

from flask import Flask, request

from .events import process_event
from .getChallenge import verify_challenge

app = Flask(__name__)


@app.route("/")
def main_handle():
    """Returns static website for Bartbot info"""
    # TODO turn this into staticly delivered website
    return """Hello! This is the main API endpoint for Bartbot. What is Bartbot you ask? Check out <a href=\"http://github.com/anwyho/bartbot\">github.com/anwyho/bartbot</a> for more details."""


@app.route("/webhook", methods=['POST', 'GET'])
def handle_webhook():
    log.basicConfig(filename='bartbot-info.log', format="%(levelname)s:%(module)s.%(funcName)s:%(lineno)d %(message)s:%(asctime)s", level=log.INFO)
    # log.basicConfig(filename='bartbot-debug.log', level=log.DEBUG)
    log.info("S T A R T I N G   L O G")
    # TODO: Verify SHA-1
    res = None
    if request.method == 'GET':
        res = verify_challenge(request)
    elif request.method == 'POST':
        res = process_event(request)
    else:
        res = "Unsupported HTTPS Verb."

    log.info("E N D I N G   L O G")
    log.shutdown()
    return res
    


if __name__ == '__main__':
    app.run()
