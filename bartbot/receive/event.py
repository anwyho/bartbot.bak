import json
import logging

from flask import request
from typing import (Generator, List, Optional, Tuple, Type, TypeVar)

# BUG: Why won't rcv.Text or rcv.Attachment work? It worked before but
#      now I have to manually import them in the two lines below
# Defined here for lazy importing
# from bartbot.receive.attachment import Attachment
# from bartbot.receive.postback import Postback
# from bartbot.receive.referral import Referral
# from bartbot.receive.text import Text
from bartbot.process.controller import (EchoController)
from bartbot.process.bartbot_controller import (BartbotController)
# from bartbot.process.controller import (import_controller)
from bartbot.send.response import (Response)
from bartbot.send.response_builder import (ResponseBuilder)


def process_event(req: request) -> list:
    """Collects and processes events"""

    data: dict = req.get_json(silent=True)
    entryList: Optional[List[dict]] = data.get('entry')

    if isinstance(entryList, list) and len(entryList) == 1 and \
            isinstance(entryList[0], dict):
        entry: dict = entryList[0]  # there should only be one entry
        objType: str = data.get('object').lower()

        if objType == 'page':
            results = handle_page_event(entry)

        elif objType == 'user':
            results = handle_user_event(entry)

        else:
            raise KeyError("Received entry had an unexpected object type.")

        return results
    else:
        raise KeyError("Received entry had an unexpected structure.")


def handle_page_event(entry: dict):
    """For each message in an entry, create and send a response."""
    # BUG: from_message() doesn't return None, but throws KeyError. If thrown, the other messages don't get processed.
    # TODO: Turn this method into a nice for loop maybe
    return list((Response.from_message(
        message=message,
        controllerType=BartbotController)  # TODO: Get from YAML
        .send()
        for message in get_messages(entry)))


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
    if isinstance(messaging, list) and len(messaging):
        for msgNum, message in enumerate(messaging):
            messageInstance = None

            # Attachments gets precedence because it can also have text
            if 'attachments' in message.get('message', {}):
                from bartbot.receive.attachment import Attachment
                messageInstance = Attachment.from_entry(
                    entry, msgNum)

            # Echo gets precedence over Text for the same reason
            elif message.get('message', {}).get('is_echo'):
                # TODO?
                # from bartbot.receive.echo import Echo
                # messageInstance = Echo.from_entry(entry, msgNum)
                pass

            elif 'text' in message.get('message', {}):
                from bartbot.receive.text import Text
                messageInstance = Text.from_entry(
                    entry, msgNum)

            elif 'postback' in message:
                from bartbot.receive.postback import Postback
                messageInstance = Postback.from_entry(
                    entry, msgNum)

            elif 'referral' in message:
                from bartbot.receive.referral import Referral
                messageInstance = Referral.from_entry(
                    entry, msgNum)

            else:
                logging.warning(f"Couldn't identify Message type. Skipping.")
                logging.debug(f"{json.dumps(entry, indent=2)}")
                pass

            if messageInstance:
                print("\nReceived message!")
                seenResponse = ResponseBuilder(
                    recipientId=messageInstance.senderId,
                    senderAction="mark_seen",
                    description="Marking message as seen")
                seenResponse.make_chained_response(
                    senderAction="typing_on",
                    description="Turning typing on")
                seenResponse.send()

                yield messageInstance

                typingOffResponse = ResponseBuilder(
                    recipientId=messageInstance.senderId,
                    senderAction="typing_off",
                    description="Turning typing off")
                typingOffResponse.send()
    else:
        logging.warning(f"Couldn't find any page events in entry.")
        logging.debug(f"{json.dumps(entry, indent=2)}")
