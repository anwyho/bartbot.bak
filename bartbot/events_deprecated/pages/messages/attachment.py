import json
import logging

from .response import send_message_to

from ....utils.phrases.phrase import get_phrase


def handle_attachment(fbId:str, attach:dict, respMsg:str) -> str:
    """Replies about attachments"""
    logging.info("Received attachment message event")
    fn, _ = get_id_name(fbId)
    msgText = get_phrase('attachment',opt={'fn' : fn})
    respMsg += send_message_to(fbId, msgText, respMsg)
    return respMsg