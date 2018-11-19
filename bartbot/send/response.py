import json
import logging
import wrapt

from typing import (List, Optional, Tuple)

from bartbot.receive.message import (Message)
from bartbot.utils.requests import (post)
from bartbot.utils.urls import (MESSAGES_API)


class Response:

    ATTACHMENT_TYPES: List[str] = [
        'image', 'audio', 'video', 'file', 'template']
    MAX_QUICK_REPLIES: int = 11
    MESSAGING_TYPES: str = ['RESPONSE', 'UPDATE', 'MESSAGE_TAG']
    NOTIFICATION_TYPES: List[Optional[str]] = [
        'regular', 'silent_push', 'no_push', None]
    QUICK_REPLY_PAYLOAD_CHAR_lIMIT = 1000
    QUICK_REPLY_TYPES: List[str] = [
        'text', 'location', 'user_phone_number', 'user_email']
    TAGS: List[Optional[str]] = [
        'community_alert',
        'confirmed_event_reminder',
        'non_promotional_subscription',
        'transportation_update',
        'feature_functionality_update',
        None]
    SENDER_ACTIONS: List[str] = ['mark_seen', 'typing_on', 'typing_off']

    class InvalidObjectStructureError(Exception):
        """
        Raised when Response has incorrect structure or is not ready to be sent.
        """
        pass

    def __init__(self,
                 apiUrl: Optional[str] = MESSAGES_API,
                 description: str = "default",
                 data: Optional[dict] = {},
                 dryRun: bool = False):
        self.apiUrl: Optional[str] = apiUrl
        self.description: str = description
        self._data: dict = data
        self._passingChecks: bool = False
        self._chainedResponse = None
        self._dryRun: bool = dryRun

    def _pre_send_check(self):
        """
        Check readiness of data before sending. Raise exceptions when
            something is wrong. Always returns True otherwise.
        """

        # TODO: Add a pre_send_check to ResponseBuilder that checks for quick_replies on the not-last-response
        # if self._chainedResponse and self.quick_replies

        # TODO: Check if everything is ready
        # NOTE: This needs to apply to both Send API objects and other objects
        if False:
            raise self.InvalidObjectStructureError(
                "Response has incorrect structure and is not ready to be sent.")

        self._passingChecks = True
        return True

    @property
    def passedChecks(self):
        self._pre_send_check()
        return self._passingChecks

    def send(self) -> List[bool]:
        """
        Check if response passes checks and then send current response and any chained responses. Return a list of bools depicting the success or failure of each successive send.
        """
        results: List[Tuple[bool, Optional[dict]]] = []
        if self._dryRun:
            print(f"DRY-RUN sent - {self.description}")
            results.extend(self.send_chained_response())

        elif self.passedChecks:
            results.append(post(self.apiUrl, json=self._data))
            if results[-1][0]:  # Successfully sent
                print(f"sent - {self.description}")
            else:  # Failed to send
                print(f"FAILED - {self.description}\n\t{results[-1][1]}")
            results.extend(self.send_chained_response())
        else:
            logging.warning("Attempted to send, unsuccessfully.")
        return results

    def send_chained_response(self):
        return self._chainedResponse.send() if isinstance(self._chainedResponse, Response) else []

    @classmethod
    def from_message(cls, message: Message, controllerType):
        return controllerType(message).produce_responses()
