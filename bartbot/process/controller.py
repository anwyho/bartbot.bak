import logging

from abc import (ABC, abstractmethod)
from concurrent.futures import (ThreadPoolExecutor)
from typing import (Optional)

from bartbot.receive.message import (Message)
from bartbot.send.response import (Response)
from bartbot.send.response_builder import (ResponseBuilder)


def import_controller(controllerName: str):
    pass


class Controller(ABC):
    def __init__(self, message: Message, dryRun: bool = False) -> None:
        self.message: Message = message
        self._dryRun: bool = dryRun
        self._executor: Optional[ThreadPoolExecutor] = None

    def produce_responses(self) -> ResponseBuilder:
        with ThreadPoolExecutor(max_workers=8) as executor:
            self._executor = executor
            self.preprocess_message()
            response = self.process_message()
            self.postprocess_message()
        return response

    @abstractmethod
    def process_message(self) -> Response:
        """
        Parse the message and generate a response to send using the
            ResponseBuilder.
        """
        pass

    def preprocess_message(self) -> None:
        pass

    def postprocess_message(self) -> None:
        pass


class EchoController(Controller):
    """Calling produce_responses from this class sends an echo of the received message."""

    def process_message(self) -> ResponseBuilder:
        return ResponseBuilder(
            recipientId=self.message.senderId,
            text=f"You typed {self.message.text if hasattr(self.message, 'text') else '[no text found]'}",
            description="Message echo from EchoController")
