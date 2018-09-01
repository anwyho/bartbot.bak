from __future__ import print_function

import hashlib
import hmac
import os
import sys

# TODO: Refresh all keys

# BART
BART_PUBL = os.environ.get('BART_PUBL')
BART_PRIV = os.environ.get('BART_PRIV')

# Dark Sky
DS_TOK = os.environ.get('DARK_SKY_PRIV')

# Facebook
FB_PAGE_ACCESS = os.environ.get('FB_PAGE_ACCESS')
FB_PAGE_ACCESS_2 = os.environ.get('FB_PAGE_ACCESS_2')
FB_VERIFY_TOK = os.environ.get('FB_VERIFY_TOKEN')

# Wit
WIT_TOK = os.environ.get('WIT_TOKEN')


def gen_app_secret_proof():
    """Calculates FB app secret proof from SHA256"""
    print("Generating app secret proof in keys.py", file=sys.stderr)
    pudding = hmac.new(FB_PAGE_ACCESS_2.encode('utf-8'),
        msg=FB_PAGE_ACCESS.encode('utf-8'),
        digestmod=hashlib.sha256).hexdigest()
    return pudding

