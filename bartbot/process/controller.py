# import boto3
import json
import logging
import wrapt

from typing import(Any, Dict, List, Optional, Tuple, Union)

from bartbot.receive.message import (Message)
from bartbot.receive.attachment import (Attachment)
from bartbot.receive.postback import (Postback)
from bartbot.receive.referral import (Referral)
from bartbot.receive.text import (Text)
from bartbot.send.response import (Response, ResponseBuilder)
from bartbot.process.user import (User)
from bartbot.utils.phrases import (Phrase)


class Controller:

    def __init__(self, message: Message) -> None:
        self.message: Message = message

    def produce_response(self) -> Response:
        resp = ResponseBuilder()

        return resp


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
