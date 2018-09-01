from __future__ import absolute_import
from __future__ import print_function

import sys

from . import keys as k

def verify_challenge(req):
    """Verifies and fulfills Messenger Platform GET challenge"""
    print("In getChallenge.verify_challenge", file=sys.stderr)
    qParams = req.args
    if qParams['hub.verify_token'] == k.FB_VERIFY_TOK and \
            qParams['hub.mode'] == 'subscribe':
        return qParams['hub.challenge']
    else: 
        return 'Invalid Request or Verification Token.'