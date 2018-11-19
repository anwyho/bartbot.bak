import json
import logging
import time
from datetime import datetime

from typing import(Optional)


class WitEntities:

    # Calculated from F1 Score from Wit Model.
    # Source:
    #   https://towardsdatascience.com/beyond-accuracy-precision-and-recall-3da06bea9f6c
    # Calculation: https://www.desmos.com/calculator/ectgpnxult
    MIN_CONFIDENCE = 0.54

    def __repr__(self):
        return f"""Intent: {self.intent}\nStation: {self.stn}\nStation Dest: {self.stnDest}\nTime: {self.time}\nTime Arr: {self.timeArr}\nDecision: {self.decision}\nGreetings? {self.greetings}\nThanks? {self.thanks}\nBye? {self.bye}"""

    def __init__(self, entities: dict):

        self.intent: Optional[str] = None
        self.stn: Optional[str] = None
        self.stnDest: Optional[str] = None
        self.time: Optional[str] = None
        self.timeArr: Optional[str] = None
        self.decision: Optional[str] = None

        self.greetings: bool = False
        self.thanks: bool = False
        self.bye: bool = False

        # print(json.dumps(entities, indent=2))

        # Handle datetime entity
        if 'datetime' in entities or \
            'dep' in entities or \
                'arr' in entities:
            def get_datetime(witTime: str):
                # print(f"witTime: {witTime}")
                dt = witTime[:19] + witTime[23:26] + witTime[27:]
                return time.strptime(dt, "%Y-%m-%dT%H:%M:%S%z") if witTime else None

            w_datetime = entities['datetime'][0]
            if 'value' == w_datetime.get('type'):
                self.time = get_datetime(self.ret_val_if_confident(w_datetime))
            elif 'interval' == w_datetime.get('type') and \
                    self.ret_val_if_confident(w_datetime, key='to'):
                self.time = get_datetime(w_datetime['from']['value'])
                self.timeArr = get_datetime(w_datetime['to']['value'])

        # Handle station entities
        if 'orig' in entities:
            self.stn = self.ret_val_if_confident(entities['orig'])
        if 'dest' in entities:
            self.stnDest = self.ret_val_if_confident(entities['dest'])
        if 'station' in entities:
            if self.stn is None:
                self.stn = self.ret_val_if_confident(entities['station'])
            else:
                self.stnDest = self.ret_val_if_confident(entities['station'])

        # Handle intents
        if 'intent' in entities:
            self.intent = self.ret_val_if_confident(entities['intent'])

        # Handle thanks
        thanks = self.ret_val_if_confident(entities.get('thanks'))
        if thanks is not None:
            self.thanks = True if thanks == 'true' else False

        # Handle greetings
        greetings = self.ret_val_if_confident(entities.get('greetings'))
        if greetings is not None:
            self.greetings = True if greetings == 'true' else False

        # Handle bye
        bye = self.ret_val_if_confident(entities.get('bye'))
        if bye is not None:
            self.bye = True if bye == 'true' else False

        # Handle decision
        if 'decision' in entities:
            self.decision = self.ret_val_if_confident(entities['decision'])

        self.handle_model_bugs()

    def handle_model_bugs(self):
        # TODO: The NLP model always recognizes "fremont" as WARM
        pass

    def ret_val_if_confident(self, entity: dict,
                             minConfidence: float = -1, key: str = 'value'):
        """
        Get the value of a Wit entity if it is above a minimum
            confidence threshold.
        """
        if minConfidence == -1:
            minConfidence = self.MIN_CONFIDENCE
        if isinstance(entity, list) and len(entity):
            entity = entity[0]
        return entity[key] if isinstance(entity, dict) and \
            entity.get('confidence', 0) > minConfidence else None
