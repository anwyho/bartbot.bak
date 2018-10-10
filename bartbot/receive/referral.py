import json
import logging

from typing import (Dict, Optional)

from bartbot.receive.message import (Message, ParamType, safe_import)


class Referral(Message):
    referralSources = ['MESSENGER_CODE', 'DISCOVER_TAB', 'ADS',
                       'SHORTLINK', 'CUSTOMER_CHAT_PLUGIN']
    referralTypes = ['OPEN_THREAD']

    def __init__(self,
                 refSource: str=None,
                 refType: str=None,
                 ref: Optional[str]=None,
                 refererUri: Optional[str]=None,
                 adId: Optional[str]=None,
                 ofPostback: bool=False,
                 **kwargs: Optional[ParamType]) -> None:

        if not ofPostback:
            super(Referral, self).__init__(messageType='REFERRAL', **kwargs)

        self.refSource: str = refSource
        self.refType: str = refType
        self.ref: Optional[str] = ref
        if self.ref:
            if self.refSource == 'CUSTOMER_CHAT_PLUGIN':
                self.refererUri: str = refererUri
            elif self.refSource == 'ADS':
                self.adId: str = adId

    @classmethod
    def _parse_referral_vars(cls, referral: dict, kwargs: dict={}) -> dict:
        if not (isinstance(referral.get('source'), str) and
                isinstance(referral.get('type'), str)):
            raise KeyError("Referrals must contain a valid source and type")

        kwargs['refSource'] = referral['source'].upper()
        kwargs['refType'] = referral['type'].upper()

        if not (referral['source'].upper() in cls.referralSources and
                referral['type'].upper() in cls.referralTypes):
            raise KeyError("Referrals must contain a valid source and type")

        kwargs['ref'] = referral.get('ref')
        kwargs['refererUri'] = referral.get('referer_uri')
        kwargs['adId'] = referral.get('ad_id')
        return kwargs

    @classmethod
    @safe_import
    def from_entry(cls, entry: dict, mNum: int):
        kwargs: Dict[str, Optional[ParamType]] = \
            super()._parse_message_vars(entry, mNum)
        kwargs = cls._parse_referral_vars(
            referral=entry['messaging'][mNum]['referral'], kwargs=kwargs)
        return Referral(**kwargs)
