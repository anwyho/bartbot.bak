
import json
import logging
import wrapt

from abc import (ABC, ABCMeta, abstractmethod)
from typing import (Any, Callable, Dict, List, Optional, Tuple, TypeVar)

from bartbot.utils.phrases import (Phrase)
from bartbot.user import (User)

Coordinate = Tuple[float, float]
ParamType = TypeVar('ParamType', str, int, Coordinate, list)


@wrapt.decorator
def safe_import(
        importer: Callable[[dict, int], Optional[Any]],
        instance, entry: dict, mNum: int) -> Any:
    """
    This wrapper attempts to catch and handle any errors that indicate
        that entries were incorrectly formatted, returning None if
        unable to import.
    """

    try:
        return importer(entry, mNum)
    except (AttributeError, IndexError, KeyError, TypeError) as e:
        logging.warning(f"Couldn't parse JSON entry. Error: {e}")
        return None


class Message(ABC):  # Message is an Abstract Base Class
    messageTypes = ['TEXT', 'ATTACHMENT', 'REFERRAL', 'POSTBACK']
    __metaclass__ = ABCMeta

    def __init__(self,
                 messageType: str,
                 pageId: str,
                 time: int,
                 senderId: str,
                 recipientId: str,
                 **kwargs: Optional[ParamType]) -> None:
        self.pageId: str = pageId
        self.time: int = time
        self.senderId: str = senderId
        self.recipientId: str = recipientId
        if messageType in self.messageTypes:
            self.messageType: str = messageType
        else:
            raise KeyError("Unsupported message type")

        if self.senderId is not None:

            self._client: User = User(id=self.senderId)
            self._phrase: Phrase = Phrase(
                initialLocale=self._client.locale)

        super().__init__()

    @staticmethod
    def _parse_message_vars(entry: dict, mNum: int, kwargs={}) -> \
            Dict[str, Optional[ParamType]]:
        """Prepare Message kwargs for subclasses"""

        messaging: dict = entry.get('messaging')
        messageType: dict = messaging[mNum] if isinstance(messaging, list) \
            and len(messaging) else None

        if messageType is None:
            raise KeyError("Couldn't find expected kind of messaging.")
        if messageType.get('isEcho'):
            raise KeyError("Message is an echo and shouldn't be processed to "
                           "avoid recursion.")

        kwargs: Dict[str, Optional[ParamType]] = {}
        kwargs["messageNumber"] = mNum
        kwargs["pageId"] = entry['id']
        kwargs["time"] = entry['time']
        kwargs["senderId"] = messageType['sender']['id']
        kwargs["recipientId"] = messageType['recipient']['id']
        return kwargs

    @classmethod
    @abstractmethod
    @safe_import
    def from_entry(cls, entry: dict, mNum: int):
        """
        Given an entry and mNum, return an instance of this object
            that is full initialized or raise an exception.
        NOTE: This function must be implemented as a @classmethod in
            every subclass.
        """
        pass
