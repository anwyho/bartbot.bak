import json
import logging

from flask import request
from typing import (Generator, List, Optional, Tuple, Type, TypeVar)

from bartbot import receive as rcv
from bartbot.process.controller import BartbotController
from bartbot.send.response import Response


def process_event(req: request) -> list:
    """Collects and processes events"""

    data: dict = req.get_json(silent=True)
    entryList: Optional[List[dict]] = data.get('entry')

    if isinstance(entryList, List[dict]) and len(entryList) == 1:
        entry: dict = entryList[0]  # there should only be one entry
        objType: str = data.get('object').lower()

        if objType == 'page':
            results = handle_page_event(entry)

        elif objType == 'user':
            results = handle_user_event(entry)

        else:
            raise KeyError("Received entry had an unexpected structure.")

        return results
    else:
        raise KeyError("Received entry had an unexpected structure.")


@Response.response_hook
def handle_page_event(entry: dict):
    """Returns a list of results from found page events"""
    # TODO: What if .generate_response() is None

    return [Response.from_message(
        message=message,
        controllerType=BartbotController)  # TODO: Get from YAML
        .build()
        .send()
        for message in get_messages(entry)]


@Response.response_hook
def handle_user_event(entry: dict):
    # results = []  # collects results of events
    # events = find_user_events(entry)
    # results.extend()
    return []


def get_messages(entry: dict):
    """
    Get specifically-typed instantiated messages from an entry
        depending on distinguishing factors in each message.
    """

    messaging = entry.get('messaging')
    if not (isinstance(messaging, list) and len(messaging)):
        logging.warning(f"Couldn't find any page events in entry.")
        logging.debug(f"{json.dumps(entry, indent=2)}")

    for msgNum, message in enumerate(messaging):
        # Attachments gets precedence because it can also have text
        if 'attachments' in message.get('message', {}):
            yield rcv.attachment.Attachment.from_entry(entry, msgNum)

        # Echo gets precedence over Text for the same reason
        elif message.get('message', {}).get('is_echo'):
            # TODO?
            # yield rcv.echo.Echo.from_entry(entry, msgNum)
            pass

        elif 'text' in message.get('message', {}):
            yield rcv.text.Text.from_entry(entry, msgNum)

        elif 'postback' in message:
            yield rcv.postback.Postback.from_entry(entry, msgNum)

        elif 'referral' in message:
            yield rcv.referral.Referral.from_entry(entry, msgNum)

        else:
            logging.warning(f"Couldn't identify Message type. Skipping.")
            logging.debug(f"{json.dumps(entry, indent=2)}")
            pass
