import json
import logging

from typing import (Dict, Optional)

from bartbot.receive.message import (
    Message, MessageParsingError, ParamType, safe_parse)
from bartbot.utils.requests import (get)
from bartbot.utils.urls import (MESSAGES_API, WIT_HEADER,
                                WIT_MESSAGE_API)


class WitParsingError(Exception):
    pass


class Text(Message):

    @safe_parse
    def __init__(self, entry: dict, mNum: int):
        super().__init__(entry=entry, mNum=mNum, messageType='TEXT')
        message = entry['messaging'][mNum]['message']
        self.messageId: str = message['mid']
        self.text: str = message['text']
        self.quickReply: Optional[str] = message.get(
            'quick_reply', {}).get('payload')
        self._witEntities: Optional[dict] = None

    @property
    def entities(self) -> Optional[dict]:
        """Only parses entities once based off of self.text"""
        # TODO: Return default response if len(self.text) > 280
        if self._witEntities is None:
            data: dict = {
                'q': self.text[:280],  # Wit has a 280 char limit
                'n': 4,  # Get 4 best entities
                'verbose': True,
                'context': json.dumps({'session_id': self.senderId})}

            ok, witResp = get(WIT_MESSAGE_API, params=data, headers=WIT_HEADER)
            if ok:
                logging.info("Successfully called Wit API")
                logging.debug(f"Wit entities: {json.dumps(witResp,indent=2)}")
                if 'entities' in witResp:
                    self._witEntities = witResp['entities']
                else:
                    logging.warning("Failed to retrieve Wit entities")
                    raise WitParsingError(
                        "Unexpected structure from Wit response.")
            else:
                raise WitParsingError("Failed to retrieve Wit entities")
        return self._witEntities
