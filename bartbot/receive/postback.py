
import json
import logging

from typing import (Dict, Optional)

from bartbot.receive.message import (Message, ParamType, safe_import)
from bartbot.receive.referral import (Referral)


class Postback(Message):
    def __init__(self,
                 title: Optional[str]=None,
                 payload: Optional[str]=None,
                 **kwargs: Optional[ParamType]) -> None:

        super(Postback, self).__init__(
            messageType='POSTBACK', **kwargs)

        self.title: str = title
        self.payload: str = payload
        try:
            self.referral: Optional[Referral] = \
                Referral(**kwargs)
        except KeyError:
            self.referral: Optional[Referral] = None

    @classmethod
    @safe_import
    def from_entry(cls, entry: dict, mNum: int):
        postback = entry['messaging'][mNum]['postback']

        kwargs: Dict[str, Optional[ParamType]] = \
            super()._parse_message_vars(entry, mNum)
        kwargs['title'] = postback['title']
        kwargs['payload'] = postback['payload']
        try:
            kwargs = Referral._parse_referral_vars(
                referral=postback.get('referral'), kwargs=kwargs)
        except KeyError:
            pass
        else:
            kwargs['ofPostback'] = True
        return cls(**kwargs)
