# import boto3
import logging
import json
import wrapt

from typing import(Any, Dict, List, Optional, Tuple, Union)

from bartbot.messages import (Message)
from bartbot.messages.attachment import (Attachment)
from bartbot.messages.postback import (Postback)
from bartbot.messages.referral import (Referral)
from bartbot.messages.text import (Text)
from bartbot.response import (Response, ResponseBuilder)
from bartbot.user import (User)
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


class Template:

    class Button:
        def __init__(self):

    def __init__(self):
