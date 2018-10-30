import logging

from abc import (ABC, abstractmethod)

from bartbot.receive.message import (Message)
from bartbot.send.response import (Response, ResponseBuilder)


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


# TODO:
# - flesh out classes below

# - media template
#   https://developers.facebook.com/docs/messenger-platform/reference/template/media

# - postback, web_url and simple share button
#   https://developers.facebook.com/docs/messenger-platform/reference/buttons/postback
#   https://developers.facebook.com/docs/messenger-platform/reference/buttons/url
#   https://developers.facebook.com/docs/messenger-platform/reference/buttons/share

# - complex share button
#   https://developers.facebook.com/docs/messenger-platform/reference/buttons/share
