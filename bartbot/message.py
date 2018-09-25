from enum import Enum
from typing import (Optional, Tuple, Union)


def setOrRaise(e, l=None):
    """
    Raise an exception when an expected keyword is None or invalid.
    """
    if e is not None and isinstance(e, str):
        if l is None or e.upper() in l:
            return e
        else:
            raise KeyError(
                f"Unexpected response structure. Unexpected value {e}.")
    else: 
        raise KeyError(
            f"Unexpected response structure. Expected a value for {e}.")


class Message:
    messageTypes = ['TEXT', 'ATTACHMENT', 'REFERRAL', 'POSTBACK']

    def __init__(self, 
            messageType:str,
            entryId:Optional[str]=None, 
            time:Optional[int]=None, 
            clientId:Optional[str]=None, 
            pageId:Optional[str]=None, 
            **kwargs):

        self.entryId:str = setOrRaise(entryId)
        self.time:int = setOrRaise(entryId)
        self.clientId:str = setOrRaise(clientId)
        self.pageId:str = setOrRaise(pageId)
        self.messageType:str = setOrRaise(messageType, 
            self.messageTypes)


class Text(Message):
    def __init__(self, 
            messageId:Optional[str]=None, 
            text:Optional[str]=None, 
            quickReply:Optional[str]=None, 
            **kwargs):

        super(Text, self).__init__(
            messageType='TEXT', **kwargs)

        self.messageId:str=setOrRaise(messageId)
        self.text:str = setOrRaise(text)
        self.quickReply:Optional[str] = quickReply


class Attachment(Message):
    attachmentTypes = ['IMAGE', 'VIDEO', 'AUDIO', 'FILE', 'LOCATION',
        'FALLBACK']

    def __init__(self,
            messageId:Optional[str]=None,  
            type:Optional[str]=None,
            text:Optional[str]=None,
            url:Optional[str]=None,
            title:Optional[str]=None,
            coordinates:Optional[Tuple[float,float]]=None, 
            **kwargs):

        super(Attachment, self).__init__(
            messageType='ATTACHMENT', **kwargs)

        self.messageId:str=setOrRaise(messageId)
        self.type:AttmType=setOrRaise(type,self.attachmentTypes)
        if self.type == 'FALLBACK':
            self.text:str = setOrRaise(text)
            self.url:str = setOrRaise(url)
        else: 
            self.title:str = setOrRaise(title)
            if self.type == 'LOCATION':
                self.coordinates:Tuple[float,float] = \
                    setOrRaise(coordinates)
            else:
                self.url:str = setOrRaise(url)


class Referral(Message):
    referralSources = ['MESSENGER_CODE', 'DISCOVER_TAB', 'ADS',
        'SHORTLINK', 'CUSTOMER_CHAT_PLUGIN']
    referralTypes = ['OPEN_THREAD']

    def __init__(self, 
            refSource:Optional[str]=None,
            refType:Optional[str]=None,
            ref:Optional[str]=None,
            refererUri:Optional[str]=None,
            adId:Optional[str]=None, 
            ofPostback:bool=False,
            **kwargs):

        if not ofPostback:
            super(Referral, self).__init__(
                messageType='REFERRAL', **kwargs)

        self.refSource:str = setOrRaise(refSource, self.referralSources)
        self.refType:str = setOrRaise(refType, self.referralTypes)
        self.ref:Optional[str] = ref
        if self.ref:
            if self.refSource == 'CUSTOMER_CHAT_PLUGIN':
                self.refererUri:str = setOrRaise(refererUri)
            elif self.refSource == 'ADS':
                self.adId:str = setOrRaise(adId)


class Postback(Message):
    def __init__(self, 
            title:Optional[str]=None,
            payload:Optional[str]=None,
            **kwargs):

        super(Postback, self).__init__(
            messageType='POSTBACK', **kwargs)

        self.title:str = setOrRaise(title)
        self.payload:str = setOrRaise(payload)
        try: 
            self.referral:Optional[Referral] = \
                Referral(ofPostback=True,**kwargs)
        except KeyError:
            self.referral:Optional[Referral] = None
