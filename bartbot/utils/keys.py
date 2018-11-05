# from __future__ import print_function

import hashlib
import hmac
import logging
import os

from typing import (Tuple)

# TODO: Refresh all keys
# TODO: Provide default values with os.environ.get("KEY", "DEFAULT")

# BART
BART_PUBL = os.environ.get('BART_PUBL')
BART_PRIV = os.environ.get('BART_PRIV')

# Facebook
FB_PAGE_ACCESS = os.environ.get('FB_PAGE_ACCESS')
FB_PAGE_ACCESS_2 = os.environ.get('FB_PAGE_ACCESS_2')
FB_VERIFY_TOK = os.environ.get('FB_VERIFY_TOK')

# Dark Sky
DS_TOK = os.environ.get('DARK_SKY_PRIV')

# Wit
WIT_TOK = os.environ.get('WIT_SERVER_TOK')

# Debug
DEBUG_TOK = os.environ.get('DEBUG_TOK')
FLASK_ENV = os.environ.get('FLASK_ENV')

_pudding = None


def gen_app_secret_proof():
    """
    Calculate FB app secret proof from SHA256 with Singleton DP
    """

    logging.info("Generating app secret proof in keys.py")

    global _pudding
    _pudding = _pudding if _pudding else \
        hmac.new(FB_PAGE_ACCESS_2.encode('utf-8'),
                 msg=FB_PAGE_ACCESS.encode('utf-8'),
                 digestmod=hashlib.sha256).hexdigest()

    return _pudding


def verify_signature(req) -> bool:
    """Verify SHA-1 of message"""
    # TODO: Verify SHA-1
    return True


def verify_challenge(queryParams: dict, respMsg: str) -> Tuple[bool, str]:
    """
    Verify and fulfill Messenger Platform GET challenge
    """

    return (True, queryParams['hub.challenge']) \
        if queryParams.get('hub.verify_token') == FB_VERIFY_TOK and \
        queryParams.get('hub.mode') == 'subscribe' and \
        isinstance(queryParams.get('hub.challenge'), str) else \
        (False, 'Invalid request or verification token.\n')
