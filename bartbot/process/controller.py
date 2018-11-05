import logging

from abc import (ABC, abstractmethod)

from bartbot.receive.message import (Message)
from bartbot.send.response import (Response)
from bartbot.send.response_builder import (ResponseBuilder)


def import_controller(controllerName: str):
    pass


class Controller(ABC):
    def __init__(self, message: Message) -> None:
        self.message: Message = message

    @abstractmethod
    def produce_responses(self) -> Response:
        """
        Parse the message and generate a response to send using the
            ResponseBuilder.
        """
        pass


class EchoController(Controller):
    """Calling produce_responses from this class sends an echo of the received message."""

    def produce_responses(self) -> ResponseBuilder:
        return ResponseBuilder(recipientId=self.message.senderId, text=f"You typed {self.message.text if hasattr(self.message, 'text') else '[no text found]'}")
