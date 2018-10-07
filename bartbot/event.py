import json
import logging

from flask import request
from typing import (Generator, List, Optional, Tuple, Type, TypeVar)

from bartbot import messages as msgs
from bartbot.controller import Controller
from bartbot.response import Response


def process_event(req: request) -> list:
    """Collects and processes events"""

    data: dict = req.get_json(silent=True)
    entryList: Optional[List[dict]] = data.get('entry')

    if isinstance(entryList, List[dict]) and len(entryList) == 1:
        entry: dict = entryList[0]  # there should only be one entry
        objType: str = data.get('object').lower()

        if objType == 'page':
            results = page_event(entry)

        elif objType == 'user':
            results = user_event(entry)

        else:
            raise KeyError("Received entry had an unexpected structure.")

        return results
    else:
        raise KeyError("Received entry had an unexpected structure.")


@Response.response_hook
def page_event(entry: dict):
    """Returns a list of results from found page events"""
    # TODO: What if .generate_response() is None

    return [Response.from_message(mType.from_entry(entry, mNum))
            .produce_response()
            .send()
            for (mType, mNum) in find_page_events(entry)]


@Response.response_hook
def user_event(entry: dict):
    # results = []  # collects results of events
    # events = find_user_events(entry)
    # results.extend()
    return []


def find_page_events(entry: dict) \
        -> List[Tuple[Optional[Type[msgs.Message], int]]]:
    """
    Collects class types based on distinguishing factors to begin
        instantiations and sending
    """

    messaging = entry.get('messaging')
    if not (isinstance(messaging, list) and len(messaging)):
        logging.warning(f"Couldn't find any page events in entry.")
        logging.debug(f"{json.dumps(entry, indent=2)}")

    for mNum, messageList in enumerate(messaging):
        # Attachments gets precedence because it can also have text
        if 'attachments' in messageList.get('message', {}):
            yield (msgs.attachment.Attachment, mNum)
        # Echo gets precedence over Text for the same reason
        elif messageList.get('message', {}).get('is_echo'):
            # TODO?
            # yield (msgs.echo.Echo, mNum)
            pass
        elif 'text' in messageList.get('message', {}):
            yield (msgs.text.Text, mNum)
        elif 'postback' in messageList:
            yield (msgs.postback.Postback, mNum)
        elif 'referral' in messageList:
            yield (msgs.referral.Referral, mNum)
        else:
            logging.warning(f"Couldn't identify Message type.")
            logging.debug(f"{json.dumps(entry, indent=2)}")
            pass
