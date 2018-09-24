import json
import logging

from typing import (Optional, Tuple)
from wit import Wit

from .response import (format_response, send_message_to)

from ....utils.keys import (DEBUG_TOK, WIT_TOK)
from ....utils.phrases.phrase import get_phrase
from ....utils.requests import get
from ....utils.urls import (MESSENGER_USER_API, WIT_HEADER, WIT_MESSAGE_API)


def handle_text(fbId:str, text:str, respMsg:str) -> str:
    logging.info("Received text message event")
    logging.debug(f"Message: {text}")

    keywordFound, msgText = handle_keywords(text)
    if keywordFound:
        logging.info("Found keyword")
        respMsg += send_message_to(fbId, msgText, respMsg)
    else: 
        msgEntities:Optional[dict] = get_msg_entities(fbId, text)
        if msgEntities is None:
            logging.warning("Couldn't get message entities from Wit")
            respMsg += handle_wit_failure(fbId, respMsg)
        else: 
            respMsg += process_message_entities(fbId, msgEntities, respMsg)
    return respMsg


def get_msg_entities(fbId:str, text:str) -> Optional[dict]:
    """Calls Wit API for natural language processing"""
    data:dict = {
        'q': text[:256],
        'n': 4,
        'verbose': True,
        'context': json.dumps({'session_id': fbId})}
    ok, witResp = get(WIT_MESSAGE_API, params=data, headers=WIT_HEADER)
    if ok:
        logging.info("Retrieved Wit entities")
        logging.debug(f"Wit entities: {json.dumps(witResp,indent=2)}")
        return witResp
    else:
        return None
        

def process_message_entities(fbId:str, msgEntities:dict, respMsg:str) -> str:
    logging.info("Processing message entities")
    if 'entities' not in msgEntities:
        respMsg += "Unexpected JSON structure. Expected 'entities' in Wit response."
    else: 
        entities:dict = msgEntities['entities']
        fn,ln = get_id_name(fbId)

        if 'greetings' in entities:
            logging.info('Sending a greeting')
            msgText = f"{get_phrase('hello', 'cta', opt={'fn' : fn})}\n"
            msgText += f"Debug info: {json.dumps(entities, indent=4)}\n"
            respMsg += send_message_to(fbId, msgText, respMsg)

        elif 'intent' in entities:
            logging.info('Parsing intent')
            intent = entities['intent'][0]['value']
            if intent == 'map':
                logging.info('Sending a map')
                respMsg += send_map_to(fbId, respMsg, fn)
            
        else:
            msgText = f"Hello {fn} {ln}. You typed: {msgEntities['_text']}"  # TODO: Is this correct? See structure of Wit entities
            respMsg += send_message_to(fbId, msgText)

    return respMsg


def handle_wit_failure(fbId:str, respMsg:str) -> str:
    # TODO: Create fallback, either message about NLP or do cheap hack
    # TODO: Link to another suitable BART schedule thing.
        # Maybe download offline schedules if can't access BART API
        # Read-access S3 bucket
    respMsg += "Can't access Wit API.\n"
    msgTxt:str = "Uh oh! I'm currently not on speaking terms with my natural language processor. Want me to let you know when I'm back online?"
    # TODO: Provide online notification subscription "Doot doot! Bartbot is fully operational!"
    respMsg += send_message_to(fbId, msgTxt, respMsg)
    return respMsg


def handle_keywords(text:str) -> Tuple[bool,Optional[str]]:
    """Checks for existence of keywords to access debugging"""
    resp:str = ""
    keywords:bool = False
    # Tests emojis and creates a palette
    if f'debug.verify_tok={DEBUG_TOK};' in text: 
    # if f'debug.verify_tok=yeaboi;' in text: 
        resp += f"{'sup fam'}\n"  # f"{'fun'}-strings"
        keywords = True
    if keywords:
        if 'print_all_emojis();' in text:
            from ...utils.phrases.emojis import print_all_emojis
            resp +=  f"{print_all_emojis()}\n"

    if resp is not "":
        return (True, resp)
    else: 
        return (False, None)


# TODO: Create User class that contains fbId with lazy attributes name and locale
def get_id_name(fbId:str) -> Tuple[str,str]:
    """
    Requests first and last name of ID from Messenger User Profile API
    https://developers.facebook.com/docs/messenger-platform/identity/user-profile/
    """

    logging.info("Getting FB name")
    queries = {'fields':['first_name','last_name']}

    ok, data = get(
        MESSENGER_USER_API.format(fbId=fbId),
        json=queries)  # TODO: Figure out why "json" works but not "params"

    if not ok:
        return ('{opt}','{opt}')
    else: 
        return (data['first_name'], data['last_name'])




# TODO: For unsure traits, offer a "find nearest" button

# TODO: Implement "yes/no" postback quick replies
#   Vary the "yes/no" e.g. "yes!/no...", "affirmative/negatory", "yep/nope"