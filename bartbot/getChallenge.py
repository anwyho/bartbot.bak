# from __future__ import absolute_import
# from __future__ import print_function

import logging

from . import keys as k

def verify_challenge(req):
    """Verifies and fulfills Messenger Platform GET challenge"""
    logging.info('In getChallenge.verify_challenge')
    qParams = req.args
    if 'hub.verify_token' in qParams.keys() and \
        'hub.mode' in qParams.keys() and \
        'hub.challenge' in qParams.keys():
        if qParams['hub.verify_token'] == k.FB_VERIFY_TOK and \
                qParams['hub.mode'] == 'subscribe':
            logging.info("Verified token.")
            return qParams['hub.challenge']
        else: 
            logging.info("Unable to verify token. Either {hubTok} != {verTok} or {hubMode} != 'subscribe'".format(
                hubTok=qParams['hub.verify_token'], 
                verTok=k.FB_VERIFY_TOK, 
                hubMode=qParams['hub.mode']))
            return 'Invalid request or verification token.'
    else: 
        logging.info("GET did not include all necessary parameters.")
        return 'Invalid request or verification token.'