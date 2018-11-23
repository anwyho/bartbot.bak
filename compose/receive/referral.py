import json
import logging

from typing import (Dict, Optional)

from compose.receive.message import (
    Message, MessageParsingError, ParamType, safe_parse)


class ReferralParsingError(Exception):
    pass


class Referral(Message):
    REFERRAL_SOURCES = ['MESSENGER_CODE', 'DISCOVER_TAB', 'ADS',
                        'SHORTLINK', 'CUSTOMER_CHAT_PLUGIN']
    REFERRAL_TYPES = ['OPEN_THREAD']

    @safe_parse
    def __init__(self, entry: dict, mNum: int, inPostback: bool = False):
        referral = entry['messaging'][mNum]['referral']

        if not (isinstance(referral.get('source'), str) and
                isinstance(referral.get('type'), str) and
                referral.get('source').upper() in self.REFERRAL_SOURCES and
                referral.get('type').upper() in self.REFERRAL_TYPES):
            raise ReferralParsingError(
                "Referrals must contain a valid source and type")

        if not inPostback:
            super().__init__(entry=entry, mNum=mNum, messageType='REFERRAL')

        self.refSource: str = referral['source'].upper()
        self.refType: str = referral['type'].upper()
        self.ref: Optional[str] = referral.get('ref')
        if self.ref:
            if self.refSource == 'CUSTOMER_CHAT_PLUGIN':
                self.refererUri: str = referral.get('referer_uri')
            elif self.refSource == 'ADS':
                self.adId: str = referral.get('ad_id')
