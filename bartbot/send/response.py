# import flask
# import gzip
import json
import logging
import wrapt

from abc import (abstractmethod)
from typing import (Any, Callable, List, Optional, Tuple, Type, Union)

from bartbot.receive.message import (Message)
from bartbot.send.button import (Button)
from bartbot.send.attachment import (Asset, Template)
from bartbot.utils.requests import (post)
from bartbot.utils.urls import (MESSAGES_API)


@wrapt.decorator
def require_rebuild(wrapped, instance, args, kwargs):
    """
    Setter wrapper that resets the built tag to `False`.
    """
    if instance:
        instance._built = False
        instance._passingChecks = False
    elif isinstance(args[0], Response):
        args[0]._built = False
        args[0]._passingChecks = False
    return wrapped(*args, **kwargs)


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
            data: Optional[dict] = {}):
        self.apiUrl: Optional[str] = apiUrl
        self._data: dict = data
        self._passingChecks: bool = False
        self._chainedResponse = None

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
        if self.passedChecks:
            results.append(post(self.apiUrl, json=self._data))
            if isinstance(self._chainedResponse, Response):
                # NOTE: Possible timout feature?
                results.extend(self._chainedResponse.send())
        else:
            logging.warning("Attempted to send, unsuccessfully.")
        return results

    @classmethod
    def from_message(cls, message: Message, controllerType):
        return controllerType(message).produce_responses()


# Interface for Send API
class ResponseBuilder(Response):
    """Provides an interface for sending to Send API"""

    def __init__(self,
                 text: str = "",
                 attachment: Optional[Union[Template, Asset]] = None,
                 messagingType: str = '',
                 metadata: str = '',
                 notificationType: str = '',
                 tag: Optional[str] = None,
                 senderAction: Optional[str] = None,
                 apiUrl: Optional[str] = MESSAGES_API,
                 **recipientArgs) -> None:
        super(ResponseBuilder, self).__init__(apiUrl=apiUrl)

        self.text: Optional[str] = text
        self._attachment: Optional[Union[Template, Asset]] = attachment if isinstance(
            attachment, Asset) else None
        self._messagingType: str = messagingType if \
            messagingType in self.MESSAGING_TYPES else 'RESPONSE'
        self._metadata: str = metadata
        self._notificationType: str = notificationType if \
            notificationType in self.NOTIFICATION_TYPES else 'regular'
        self._tag: Optional[str] = tag
        self._senderAction: Optional[str] = senderAction
        self.quickReplies: List[dict] = []
        if recipientArgs:
            self.set_recipient(**recipientArgs)
        self._built: bool = False

    @classmethod
    def generate_indicators(cls, fbId: str):
        """
        Yields Responses for sending message indicators to a given Facebook ID.
        """
        if not fbId:
            yield None
        else:
            yield True
        resp = cls(senderAction='mark_seen', recipientId=fbId)
        yield resp
        resp.senderAction = 'typing_on'
        yield resp
        resp.senderAction = 'typing_off'
        yield resp

    def make_chained_response(self, **responseInitKwargs):
        """Create and attach a chained response and set recipient."""
        self._chainedResponse = ResponseBuilder(**responseInitKwargs)
        self._chainedResponse._recipient = self._recipient
        return self._chainedResponse

    def make_separate_response(self, **responseInitKwargs):
        """Create a new response set the same recipient."""
        resp = ResponseBuilder(**responseInitKwargs)
        resp._recipient = self._recipient
        return resp

    @property
    def attachment(self):
        return self._attachment

    @attachment.setter
    @require_rebuild
    def attachment(self, templateOrAsset: Union[Template, Asset]):
        if isinstance(templateOrAsset, Template) or \
                isinstance(templateOrAsset, Asset):
            self._attachment = templateOrAsset
        else:
            ValueError(
                "Attempted to set attachment to object other than Template or Asset.")

    @property
    def messagingType(self) -> str:
        return self._messagingType

    @messagingType.setter
    @require_rebuild
    def messagingType(self, messagingType: str) -> None:
        if messagingType in self.MESSAGING_TYPES:
            self._messagingType = messagingType
        else:
            ValueError(
                f"Attempted to set messaging type to an unsupported messaging type {messagingType}.")

    @property
    def metadata(self) -> str:
        return self._metadata

    @metadata.setter
    @require_rebuild
    def metadata(self, metadata: str) -> None:
        self._metadata = metadata

    @property
    def notificationType(self) -> str:
        return self._notificationType

    @notificationType.setter
    @require_rebuild
    def notificationType(self, notificationType: str) -> None:
        if notificationType in self.NOTIFICATION_TYPES:
            self._notificationType = notificationType
        else:
            ValueError(
                f"Attempted to set notification type to an unsupported messaging type {notificationType}.")

    def recipient(self) -> dict:
        return self._recipient

    @require_rebuild
    def set_recipient(self,
                      recipientId: Optional[str] = None,
                      phoneNumber: Optional[str] = None,
                      firstName: Optional[str] = None,
                      lastName: Optional[str] = None,
                      userRef: Optional[str] = None) -> None:
        """
        Set recipient information with Facebook ID taking priority, followed by phone number and then user referral.
        """

        if recipientId:
            self._recipient: dict = {'id': recipientId}
        elif phoneNumber:
            self._recipient: dict = {
                'id': phoneNumber, 'phone_number': phoneNumber}
            if firstName and lastName:
                self._recipient['name']: dict = {
                    'first_name': firstName, 'last_name': lastName}
        elif userRef:
            self._recipient: dict = {'id': userRef, 'user_ref': userRef}
        else:
            logging.debug(
                f"Failed to set recipient info. Variable dump: \nrecipientId: {recipientId}\nphoneNumber: {phoneNumber}\nfirstName: {firstName}\nlastName: {lastName}\nuserRef: {userRef}")
            raise ValueError("Failed to set recipient information.")

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    @require_rebuild
    def tag(self, tag: str) -> None:
        if tag in self.TAGS:
            self._tag = tag
        else:
            ValueError(
                f"Attempted to set tag to an unsupported tag {tag}.")

    @property
    def senderAction(self) -> str:
        return self._senderAction

    @senderAction.setter
    @require_rebuild
    def senderAction(self, senderAction: str) -> None:
        if senderAction in self.SENDER_ACTIONS:
            self._senderAction = senderAction
        else:
            ValueError(
                f"Attempted to set sender action to an unsupported sender action {senderAction}.")

    @require_rebuild
    def add_quick_reply(self,
                        contentType: str = 'text',
                        text: str = '',
                        postbackPayload: Union[str, int] = '',
                        imageUrl: str = '') -> dict:
        """
        Add a quick-reply to the message payload. Remove quick-reply not implemented yet.
        """

        if len(self.quickReplies) >= self.MAX_QUICK_REPLIES:
            raise ValueError(
                f"Only {self.MAX_QUICK_REPLIES} quick replies are allowed per response.")
        contentType = contentType.lower()
        if contentType in self.QUICK_REPLY_TYPES:
            quickReply: dict = {'content_type': contentType}
            if contentType == 'text':
                quickReply['title'] = text
                quickReply['payload'] = postbackPayload
                if imageUrl or text == '':
                    if imageUrl:
                        quickReply['image_url'] = imageUrl
                    else:
                        raise ValueError(
                            "Expected image URL with empty title string.")
            self.quickReplies.append(quickReply)
        else:
            raise ValueError(
                "Attempted to create unsupported quick reply type.")

    def build(self):
        if self._built:
            return

        self._data: dict = {}

        self._data['messaging_type'] = self.messagingType
        self._data['recipient'] = self.recipient()

        if self.text or self.attachment:
            message: dict = {}

            if self.text:
                message['text'] = self.text
            elif self.attachment:
                message['attachment'] = self.attachment.build()
            else:
                raise ValueError("Expected either text or attachment.")

            if self.quickReplies:
                message['quick_replies'] = self.quickReplies
            if self.metadata:
                message['metadata'] = self.metadata
            self._data['message'] = message

            self._data['notification_type'] = self.notificationType
            if self.tag:
                self._data['tag'] = self.tag

        elif self.senderAction is not None:
            self._data['sender_action'] = self.senderAction

        self._built = True

    def send(self) -> bool:
        """
        Verify that response data is built before calling super send method.
        """
        if not self._built:
            self.build()
        return super(ResponseBuilder, self).send()
