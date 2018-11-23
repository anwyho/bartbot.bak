
import json
import logging

from typing import (Dict, Optional)

from compose.receive.message import (
    Message, MessageParsingError, ParamType, safe_parse)
from compose.receive.referral import (Referral, ReferralParsingError)


class Postback(Message):

    @safe_parse
    def __init__(self, entry: dict, mNum: int):
        super().__init__(entry=entry, mNum=mNum, messageType='POSTBACK')
        postback = entry['messaging'][mNum]['postback']
        self.title: str = postback['title']
        self.payload = postback['payload']
        try:
            self.referral: Optional[Referral] = Referral(
                entry=entry, mNum=mNum, inPostback=True)
        except ReferralParsingError:
            self.referral: Optional[Referral] = None
