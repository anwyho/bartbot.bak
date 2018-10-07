# import flask
import json
import logging
import wrapt

from typing import (Any, Callable, List, Optional)

# Defined within Response to prevent circular imports
# from bartbot.controller import Controller
from bartbot.messages import (Message)
from bartbot.utils.requests import (post)
from bartbot.utils.urls import (MESSAGES_API)


class Response():
    MESSAGING_TYPES: str = ['RESPONSE', 'UPDATE', 'MESSAGE_TAG']
    NOTIFICATION_TYPES: List[Optional[str]] = [
        'REGULAR', 'SILENT_PUSH', 'NO_PUSH', None]
    TAGS: List[Optional[str]] = [
        'COMMUNITY_ALERT',
        'CONFIRMED_EVENT_REMINDER',
        'NON_PROMOTIONAL_SUBSCRIPTION',
        'TRANSPORTATION_UPDATE',
        'FEATURE_FUNCTIONALITY_UPDATE',
        None]
    ATTACHMENT_TYPES: List[Optional[str]] = [
        'image', 'audio', 'video', 'file', 'template', None]
    TEMPLATE_TYPES: List[Optional[str]] = [
        'generic',
        'button',
        'list',
        'media',
        # 'receipt',  # not currently supported
        None]
    BUTTON_TYPES: List[Optional[str]] = [
        'web_url',
        'postback',
        'element_share',
        'phone_number',
        None]
    QUICK_REPLY_TYPES: List[Optional[str]] = [
        'text', 'location', 'user_phone_number', 'user_email']
    MAX_QUICK_REPLIES: int = 11

    def __init__(self, apiUrl: Optional[str]=MESSAGES_API) -> None:
        self.url: Optional[str] = apiUrl
        self.data = {}
        self._readyToSend: bool = False

    def send(self) -> bool:
        isOk = False
        if self._readyToSend:
            isOk = post(self.url, json=self.data)[0]
        else:
            logging.warning("Attempted to send, unsuccessfully.")
        return isOk

    @classmethod
    def from_message(cls, message: Message):
        from bartbot.controller import Controller
        return Controller(message).produce_response()

    @classmethod
    def generate_indicators(cls, fbId: str):
        """A generator function that yields Responses for sending"""
        if not fbId:
            yield None
        else:
            yield
        resp = ResponseBuilder()
        resp._messagingType = 'RESPONSE'
        resp._recipientId = fbId
        resp._senderAction = 'mark_seen'
        resp._readyToSend = True
        yield resp
        resp._senderAction = 'typing_on'
        yield resp
        resp._senderAction = 'typing_off'
        yield resp

    @staticmethod
    @wrapt.decorator
    def response_hook(
        event_handler: Callable[[dict], Optional[Any]],
            instance, entry: dict) -> Any:
        """Provides a wrapper for handling events"""

        # Pre-Handle Hook
        successfulGen = []
        for messagingObj in entry.get('messaging', []):
            if isinstance(messagingObj, dict):
                fbId = messagingObj.get('sender', {}).get('id', "")
                gen = Response.generate_indicators(fbId)
                if next(gen):
                    next(gen).send()  # mark_seen
                    next(gen).send()  # typing_on
                    successfulGen.append(gen)
        # End Pre-Handle Hook

        # Call event handler and capture result
        result = event_handler(entry)

        # Post-Handle Hook
        for gen in successfulGen:
            next(gen).send()  # typing_off
        # End Post-Handle Hook

        return result


# Interface for Send API
class ResponseBuilder(Response):
    """Provides an interface for sending to Send API"""

    def __init__(self,
                 messagingType: str='RESPONSE',
                 text: Optional[str]=None,
                 **kwargs) -> None:
        super(ResponseBuilder, self).__init__(**kwargs)

        self.text: Optional[str] = text
        self._messagingType: Optional[str] = messagingType
        self._attachmentId: Optional[str] = attachmentId
        self._quickReplies: List[dict] = []

    @property
    def messagingType(self) -> str:
        return self._messagingType

    @messagingType.setter
    def messagingType(self, messagingType: str) -> None:
        if messagingType in self.MESSAGING_TYPES:
            self._messagingType = messagingType

    @property
    def notificationType(self) -> str:
        return self._notificationType

    @notificationType.setter
    def notificationType(self, notificationType: str) -> None:
        if notificationType in self.NOTIFICATION_TYPES:
            self._notificationType = notificationType

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    def tag(self, tag: str) -> None:
        if tag in self.TAGS:
            self._tag = tag

    @property
    def metadata(self) -> str:
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: str) -> None:
        if metadata:
            self._metadata = metadata

    @property
    def recipient(self) -> dict:
        return self._recipient

    @recipient.setter
    def recipient(self,
                  id: Optional[str] = None,
                  phoneNumber: Optional[str] = None,
                  firstName: Optional[str] = None,
                  lastName: Optional[str] = None,
                  userRef: Optional[str] = None) -> None:
        if id:
            self._recipient: dict = {'id': id}
        elif phoneNumber:
            self._recipient: dict = {
                'id': phone_number, 'phone_number': phoneNumber}
            if firstName and lastName:
                self._recipient['name']: dict = {
                    'first_name': firstName, 'last_name': lastName}}
        elif userRef:
            self._recipient: dict = {'id': userRef, 'user_ref': userRef}
        else:
            logging.warning("Couldn't set recipient successfully.")

    def build(self):

        self._data = {}



    def make_template(self,
            templateType = 'GENERIC'):
        pass

    def add_quick_reply(self,
            contentType: str = 'Text',
            title: str = '',
            postbackPayload: Union[str, int] = '',
            imageUrl: str = '') -> None:
        if len(self._quickReplies) >= MAX_QUICK_REPLIES:
            logging.warning('Only ')
        if contentType in self.QUICK_REPLY_TYPES:
            quickReply: dict={'content_type': contentType}
            if contentType == 'Text':
                quickReply['title']=title
                quickReply['payload']=postbackPayload
                if imageUrl:
                    quickReply['image_url']=imageUrl
            self._quickReplies.append(quickReply)
        else:
            logging.warning(
                "Attempted to create unsupported quick reply type.")

    def add_button(self, buttonType = 'WEB_URL'):
        self._button
