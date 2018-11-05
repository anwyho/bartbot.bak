import json
import logging

from typing import (Dict, List, Optional, Tuple, Union)

from bartbot.receive.message import (Coordinate, Message, safe_import)
from bartbot.receive.message import (ParamType)


class Payload():
    def __init__(self,
                 attmType: str=None,
                 coordinates: Coordinate = None,
                 text: Optional[str] = None,
                 title: str = None,
                 url: str = None) -> None:
        self.attmType: str = attmType
        self.text: Optional[str] = text
        self.title: Optional[str] = title
        if self.attmType == 'LOCATION':
            self.coordinates: Coordinate = coordinates
        else:
            self.url = url

    @staticmethod
    def parse_payload_vars(attachment: dict, text: str) -> \
            Dict[str, Optional[Union[str, Tuple[float, float]]]]:
        attmType = attachment['type']
        coordinates: Optional[dict] = attachment['payload'].get('coordinates')

        kwargs: Dict[str, Optional[Union[str, Tuple[float, float]]]] = {}
        kwargs["attmType"] = attmType.upper()
        kwargs["coordinates"] = (coordinates['long'], coordinates['lat']) \
            if coordinates else None
        kwargs["text"] = text if attmType == 'FALLBACK' \
            else None
        kwargs["title"] = attachment['title'] if attmType == 'FALLBACK' \
            else None
        kwargs["url"] = attachment['url'] if attmType == 'FALLBACK' \
            else attachment['payload'].get('url')
        return kwargs


class Attachment(Message):
    attachmentTypes = ['IMAGE', 'VIDEO', 'AUDIO', 'FILE', 'LOCATION',
                       'FALLBACK']

    def __init__(self,
                 attachments: List[Payload]=None,
                 messageId: str=None,
                 **kwargs: Optional[ParamType]) -> None:
        super(Attachment, self).__init__(
            messageType='ATTACHMENT', **kwargs)
        self.messageId: str = messageId
        self.attachments: List[Payload] = attachments

    @classmethod
    @safe_import
    def from_entry(cls, entry: dict, mNum: int):
        """
        Parse entry in Message and then each individual attachment
        Should only throw KeyErrors
        """

        messageList = entry['messaging']
        message = messageList[mNum]['message']
        attachmentList = message['attachments']

        kwargs: Dict[str, Optional[ParamType]] = \
            super()._parse_message_vars(entry, mNum)
        kwargs['messageId'] = message['mid']
        kwargs['attachments'] = []

        # Parse each attachment and append to kwargs['attachments']
        for attachment in attachmentList:
            attmType = attachment['type']
            if not isinstance(attmType, str) or attmType.upper() not in \
                    cls.attachmentTypes:
                raise KeyError(f"Received invalid attachment type {attmType}")
            kwargs['attachments'].append(
                Payload(**Payload.parse_payload_vars(
                    attachment, message.get('text'))))

        return cls(**kwargs)
