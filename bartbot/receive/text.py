import json
import logging

from typing import (Dict, Optional)

from bartbot.receive.message import (Message, ParamType, safe_import)
from bartbot.utils.requests import (get)
from bartbot.utils.urls import (MESSAGES_API, WIT_HEADER,
                                WIT_MESSAGE_API)


class Text(Message):

    def __init__(self,
                 messageId: str,
                 text: str,
                 quickReply: Optional[str] = None,
                 **kwargs: Optional[ParamType]) -> None:
        """Constructor for Text object. Calls Message constructor."""
        super(Text, self).__init__(
            messageType='TEXT', **kwargs)

        self.messageId: str = messageId
        self.text: str = text
        self.quickReply: Optional[str] = quickReply
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
                logging.info("Successfully retrieved Wit entities")
                logging.debug(f"Wit entities: {json.dumps(witResp,indent=2)}")
                if 'entities' not in witResp:
                    logging.warning("Failed to retrieve Wit entities")
                    raise KeyError("Unexpected structure from Wit response.")
                else:
                    self._witEntities = witResp['entities']
            else:
                logging.warning("Failed to retrieve Wit entities")
                return None
        return self._witEntities
        # {
        #     "intent": [
        #         {
        #             "confidence": 0.9996880040735,
        #             "value": "map",
        #             "_entity": "intent"
        #         },
        #         {
        #             "confidence": 0.00013442298169662,
        #             "value": "help",
        #             "_entity": "intent"
        #         },
        #         {
        #             "confidence": 3.9605147030204e-05,
        #             "value": "travel",
        #             "_entity": "intent"
        #         },
        #         {
        #             "confidence": 1.5016054927827e-05,
        #             "value": "cost",
        #             "_entity": "intent"
        #         }
        #     ],
        #     "decision": [
        #         {
        #             "confidence": 4.4354493420279e-05,
        #             "value": "yes",
        #             "_entity": "decision"
        #         },
        #         {
        #             "confidence": 1.1067228903365e-05,
        #             "value": "no",
        #             "_entity": "decision"
        #         }
        #     ],
        #     "greetings": [
        #         {
        #             "confidence": 0.0020849342089947,
        #             "value": "true",
        #             "_entity": "greetings"
        #         }
        #     ],
        #     "thanks": [
        #         {
        #             "confidence": 0.00022431994258195,
        #             "value": "true",
        #             "_entity": "thanks"
        #         }
        #     ],
        #     "bye": [
        #         {
        #             "confidence": 0.0075319464344856,
        #             "value": "true",
        #             "_entity": "bye"
        #         }
        #     ]
        # }

    @safe_import
    @classmethod
    def from_entry(cls, entry: dict, mNum: int):
        """
        Parse message num mNum in given entry for arguments necessary
            to instantiate Text object
        """
        message = entry['messaging'][mNum]['message']

        kwargs: Dict[str, Optional[ParamType]] = \
            super()._parse_message_vars(entry, mNum)
        kwargs['messageId'] = message['mid']
        kwargs['text'] = message['text']
        kwargs['quickReply'] = message.get('quick_reply', {}).get('payload')
        return cls(**kwargs)
