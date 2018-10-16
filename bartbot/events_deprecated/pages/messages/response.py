import json
import logging
import os

from typing import (Tuple)

from ....resources import map_post as bartMap
from ....utils.requests import (get, post)
from ....utils.urls import (MESSAGES_API)


def format_response():
    pass


def send_message_to(fbId:str, text:str, respMsg:str) -> str:
    """Returns response to Messenger via Send API"""
    # NOTE: Handles 2000 character message limit
    sentSuccess = True
    while text != "":
        message = text[:1996]
        logging.info(f"Sending message '{text}' to FB ID {fbId}")
        data = {
            'messaging_type': 'RESPONSE',
            'recipient': {'id': fbId},
            'message': {'text': message}}

        sentSuccess = post(MESSAGES_API, json=data)[0] and sentSuccess
        text = text[1996:]
    respMsg += "Sent message successfully" if sentSuccess else "Something went wrong while sending message."
    return respMsg


def send_map_to(fbId:str, respMsg:str, fn:str='{opt}') -> Tuple[str, str]:
    """Sends a map using Messenger Attachment and returns delivery phrase"""
    logging.info('Sending a map')
    logging.debug(f'fbId: {fbId}')

    mapId = bartMap.get_map_id()
    if mapId != None: 
        data = {
            'recipient': {'id': fbId},
            'messaging_type': 'RESPONSE',
            'message': {
                'attachment': {
                    'type': 'image',
                    'payload': {
                        'attachment_id': mapId}}}}

        # TODO: Maybe batch map and message?
        

        sentSuccess = post(MESSAGES_API, json=data)[0]
        return get_phrase('delivery', opt={'fn' : fn})
    else: 
        # HACK: Make this better
        return 'Check here! http://www.bart.gov/stations'