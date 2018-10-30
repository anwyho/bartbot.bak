# import boto3
import json
import logging
import wrapt

from abc import (ABC, abstractmethod)
from typing import(Any, Dict, List, Optional, Tuple, Union)

from bartbot import receive as rcv
from bartbot.process.controller import (Controller)
from bartbot.send.attachment import (Asset, Template)
from bartbot.send.button import (Button)
from bartbot.send.response import (Response, ResponseBuilder)
from bartbot.resources.map import (yield_map_id)


class BartbotController(Controller):
    def produce_responses(self) -> ResponseBuilder:
        head = ResponseBuilder(recipientId=self.message.senderId)
        nextResp = head

        if isinstance(self.message, rcv.attachment.Attachment):
            nextResp.text = self.message._phrase.get_phrase(
                'attachment', opt={'fn': self.message._client.fn})

        elif isinstance(self.message, rcv.text.Text):
            nextResp.text = f"You typed {self.message.text}\n"
            # nextResp = nextResp.make_chained_response(
            #     text=f"Debug info: \n{json.dumps(self.message.entities, indent=2)}")

            if self.message.entities.get('greetings', [{}])[0].get(
                    'confidence', 0) > 0.7:

                nextResp = nextResp.make_chained_response(
                    text=self.message._phrase.get_phrase(
                        'hello', 'cta', opt={'fn': self.message._client.fn}))

            # if self.message.entities.get('map', [{}])[0].get(
                # 'confidence', 0) > 0.7:
            if 'map' == self.message.entities.get('intent', [{}])[0].get('value', ''):
                nextResp = self.intent_map(nextResp)

            nextResp.add_quick_reply(
                text="Break Bartbot", postbackPayload="Payload")
            nextResp.add_quick_reply(
                text="Break Bartbot Pt. 2", postbackPayload="Payload")

        return head

    def send_waiting_response(self, responseSkeleton):
        responseSkeleton.text = self.message._phrase.get_phrase(
            'wait', opt={'fn': self.message._client.fn})
        responseSkeleton.make_chained_response(senderAction="typing_on")
        responseSkeleton.send()

    def intent_map(self, nextResp: ResponseBuilder) -> ResponseBuilder:
        nextResp = nextResp.make_chained_response(
            text=self.message._phrase.get_phrase(
                'delivery', opt={'fn': self.message._client.fn}))
        mapIdGen = yield_map_id()
        mapId = next(mapIdGen)
        if not mapId:
            self.send_waiting_response(
                responseSkeleton=nextResp.make_separate_response())
            mapId = next(mapIdGen)
        if mapId:
            nextResp = nextResp.make_chained_response(
                attachment=Asset(assetType='image', attchId=mapId))
        else:
            # TODO: Backup plan
            pass

        return nextResp
