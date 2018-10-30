# import boto3
import json
import logging
import wrapt

from abc import (ABC, abstractmethod)
from typing import(Any, Dict, List, Optional, Tuple, Union)

from bartbot.process.user import (User)
from bartbot.receive.message import (Message)
from bartbot.receive.attachment import (Attachment as Attachment)
from bartbot.receive.postback import (Postback)
from bartbot.receive.referral import (Referral)
from bartbot.receive.text import (Text)
from bartbot.send.attachment import (Asset, Template)
from bartbot.send.button import (Button)
from bartbot.send.response import (Response, ResponseBuilder)
from bartbot.resources.map import (get_map_id)
from bartbot.utils.phrases import (Phrase)


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
    pass


class BartbotEnController(Controller):
    def produce_responses(self) -> Response:
        head = ResponseBuilder(recipientId=self.message.senderId)
        nextResp = head

        if isinstance(self.message, Attachment):
            nextResp.text = self.message._phrase.get_phrase(
                'attachment', opt={'fn': self.message._client.fn})

        elif isinstance(self.message, Text):
            nextResp.text = f"You typed {self.message.text}\n"
            nextResp = nextResp.make_chained_response(
                text=f"Debug info: \n{json.dumps(self.message.entities, indent=2)}")

            if self.message.entities.get('greetings', [{}])[0].get(
                    'confidence', 0) > 0.7:

                nextResp = nextResp.make_chained_response(
                    text=self.message._phrase.get_phrase(
                        'hello', 'cta', opt={'fn': self.message._client.fn}))

            # if self.message.entities.get('map', [{}])[0].get(
                # 'confidence', 0) > 0.7:
            if 'map' == self.message.entities.get('intent', [{}])[0].get('value', ''):

                nextResp = nextResp.make_chained_response(
                    text=self.message._phrase.get_phrase(
                        'delivery', opt={'fn': self.message._client.fn}))
                mapId = get_map_id()
                if mapId:
                    nextResp = nextResp.make_chained_response(
                        attachment=Asset(assetType='image', attchId=mapId))
                else:
                    # TODO: Backup plan
                    pass

                nextResp.add_quick_reply(
                    text="Break Bartbot", postbackPayload="Payload")
                nextResp.add_quick_reply(
                    text="Break Bartbot Pt. 2", postbackPayload="Payload")

        return head


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
