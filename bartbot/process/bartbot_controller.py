# import boto3
import json
import logging
import time
import wrapt

from abc import (ABC, abstractmethod)
from typing import(Any, Dict, List, Optional, Tuple, Union)

from bartbot import receive as rcv
from bartbot.process.controller import (Controller)
from bartbot.process.entities import (WitEntities)
from bartbot.send.attachment import (Asset, Template)
from bartbot.send.button import (Button)
from bartbot.send.response import (Response)
from bartbot.send.response_builder import (ResponseBuilder)
from bartbot.receive.attachment import (Attachment)
from bartbot.resources.map import (yield_map_id)


class BartbotController(Controller):

    HELP_TEXT = "[TODO: Fill in this help text.]"

    def produce_responses(self) -> ResponseBuilder:
        head = ResponseBuilder(recipientId=self.message.senderId)
        respTail = head

        head.text = f'You typed: "{self.message.text}"'
        head.description = "Echoing message"

        if isinstance(self.message, Attachment):
            respTail = respTail.make_chained_response()
            respTail.text = self.message._phrase.get_phrase(
                'attachment', opt={'fn': self.message._client.fn})
            respTail.description = "Attachment response"

        elif isinstance(self.message, rcv.text.Text):
            respTail = respTail.make_chained_response()
            entities = WitEntities(self.message.entities)
            respTail.text = str(entities)
            respTail.description = "Wit entities"

            intent = entities.intent
            if 'help' == intent:
                respTail = self.help_response(respTail)
            elif 'map' == intent:
                respTail = self.map_response(respTail)
            elif 'travel' == intent:
                respTail = self.travel_response(respTail)
            elif 'single-trip-cost' == intent:
                respTail = self.cost_response(respTail)
            elif 'round-trip-cost' == intent:
                respTail = self.cost_response(respTail, roundTrip=True)
            elif 'weather' == intent:
                respTail = self.weather_response(respTail)
            elif 'reset' == intent:
                respTail = self.reset_response(respTail)
            else:
                pass

            respTail.add_quick_reply(
                text="What is love?", postbackPayload="Payload")
            respTail.add_quick_reply(
                text="Baby don't hurt me...", postbackPayload="Payload")

        return head

    def help_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail = respTail.make_chained_response(
            text=self.HELP_TEXT,
            description="Help text response")
        return respTail

    def map_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail = respTail.make_chained_response(
            text=self.message._phrase.get_phrase(
                'delivery', opt={'fn': self.message._client.fn}),
            description="Delivery text")
        mapIdGen = yield_map_id()
        mapId = next(mapIdGen)
        if not mapId:
            self.send_waiting_response(respTail)
            mapId = next(mapIdGen)
        if mapId:
            respTail = respTail.make_chained_response(
                attachment=Asset(assetType='image', attchId=mapId),
                description="Map asset from attachment ID")
        else:
            # TODO: Backup plan
            pass

        return respTail

    def cost_response(self, respTail: ResponseBuilder, roundTrip: bool = False) -> ResponseBuilder:
        respTail.make_chained_response(
            text="[TODO: Fill in the cost response.]",
            description="Cost text")
        return respTail

    def travel_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail.make_chained_response(
            text="[TODO: Fill in the travel response.]",
            description="Travel text")
        return respTail

    def weather_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail.make_chained_response(
            text="[TODO: Fill in the weather response.]",
            description="Weather text")
        return respTail

    def reset_response(self, respTail: ResponseBuilder) -> ResponseBuilder:
        respTail.make_chained_response(
            text="[TODO: Fill in the reset response.]",
            description="Reset text")
        return respTail

    def send_waiting_response(self, respTail: ResponseBuilder):
        respBranch = respTail.make_separate_response(description="Wait text")
        respBranch.text = self.message._phrase.get_phrase(
            'wait', opt={'fn': self.message._client.fn})
        respBranch.make_chained_response(
            senderAction="typing_on",
            description="Turn typing on")
        respBranch.send()
