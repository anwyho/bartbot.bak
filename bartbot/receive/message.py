
import json
import logging
import wrapt

from abc import (ABC, ABCMeta, abstractmethod)
from typing import (Any, Callable, Dict, List, Optional, Tuple, TypeVar)

from bartbot.utils.errors import (print_traceback)
from bartbot.utils.phrases import (Phrase)
from bartbot.process.user import (User)

Coordinate = Tuple[float, float]
ParamType = TypeVar('ParamType', str, int, Coordinate, list)


class MessageParsingError(Exception):
    pass


@wrapt.decorator
def safe_parse(wrapped, instance, args, kwargs):
    """
    This wrapper attempts to catch and handle any errors that indicate
        that entries were incorrectly formatted, returning None if
        unable to import.
    """

    try:
        return wrapped(*args, **kwargs)
    except (AttributeError, IndexError, KeyError, TypeError) as e:
        raise MessageParsingError(f"Couldn't parse JSON entry. Error: {e}")
    except Exception as e:
        print_traceback(e)


class Message(ABC):  # Message is an Abstract Base Class
    SUPPORTED_MESSAGE_TYPES = ['TEXT', 'ATTACHMENT', 'REFERRAL', 'POSTBACK']
    __metaclass__ = ABCMeta

    @safe_parse
    def __init__(self, entry: dict, mNum: int, messageType: str):
        print(entry)
        messaging: dict = entry['messaging'][mNum]

        if messageType in self.SUPPORTED_MESSAGE_TYPES:
            self.messageType: str = messageType
        else:
            raise MessageParsingError("Unsupported message type")

        self.messageNum = mNum  # NOTE: This is deprecated
        self.pageId: str = entry['id']
        self.time: int = entry['time']
        self.senderId: str = messaging['sender']['id']
        self.recipientId: str = messaging['recipient']['id']

        if self.senderId is not None:
            self._client: User = User(id=self.senderId)
            # HACK: Phrase is not complete
            self._phrase: Phrase = Phrase(
                initialLocale=self._client.locale)
