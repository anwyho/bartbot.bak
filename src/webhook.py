from __future__ import absolute_import
from __future__ import print_function

import sys

from flask import Flask, request

from .getChallenge import verify_challenge
from .processMessages import process_messages_event

app = Flask(__name__)


@app.route("/")
def main_handle():
    """Returns static website for Bartbot info"""
    print("In main handle", file=sys.stderr)
    # TODO turn this into staticly delivered website
    return """Hello! This is the main API endpoint for Bartbot. What is Bartbot you ask? Check out <a href=\"http://github.com/anwyho/bartbot\">github.com/anwyho/bartbot</a> for more details."""


@app.route("/webhook", methods=['POST', 'GET'])
def handle_webhook():
    print("In webhook", file=sys.stderr)
    # TODO: Verify SHA-1
    if request.method == 'GET':
        return verify_challenge(request)
    elif request.method == 'POST':
        return process_messages_event(request)
    else:
        return "Unsupported HTTPS Verb."


if __name__ == '__main__':
    app.run()
