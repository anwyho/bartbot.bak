import json
import logging

from .attachment import handle_attachment
from .text import handle_text


def handle_message(fbId:str, message:dict, respMsg:str) -> str:
    """Decides whether to process for text or attachments"""
    logging.debug(f"Message: {json.dumps(message,indent=2)}")

    if 'text' in message.keys():
        respMsg += handle_text(fbId, message['text'], respMsg)

    elif 'attachments' in message.keys():
        respMsg += handle_attachment(fbId, message['attachments'], respMsg)

    else: 
        logging.warning("Received empty message event")
        respMsg += "Message body is empty.\n"

    return respMsg
