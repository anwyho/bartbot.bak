
import json
import logging

from abc import (ABC, abstractmethod)
from typing import (List, Optional)

from bartbot.send import (set_if_exists)

# # Defined below to avoid circular dependencies
# from bartbot.send.attachment import ShareTemplate


class Button(ABC):

    BUTTON_TYPES: List[Optional[str]] = [
        'web_url',
        'postback',
        'element_share',
        'phone_number',
        None]

    BUTTON_TITLE_CHAR_LIMIT = 20

    @classmethod
    def make_button(cls, buttonType: str, **kwargs):
        buttonType = buttonType.lower()
        if buttonType == 'web_url':
            return UrlButton(**kwargs)
        elif buttonType == 'postback':
            return PostbackButton(**kwargs)
        elif buttonType == 'element_share':
            return ShareButton(**kwargs)
        elif buttonType == 'phone_number':
            return CallButton(**kwargs)
        else:
            logging.warning(
                f"Attempted to make unsupported button type {buttonType}.")

    @abstractmethod
    def build(self) -> dict:
        """Builds itself as a dict to be placed into a built template"""
        pass


# DONE
class UrlButton(Button):

    TITLE_CHAR_LIMIT = 20
    WEB_VIEW_HEIGHT_RATIOS = ['compact', 'tall', 'full']

    def __init__(self,
                 text: str,
                 url: str,
                 messengerExtensions: bool = False,
                 fallbackUrl: Optional[str] = None,
                 webviewHeightRatio: Optional[str] = None,
                 webviewShareButton: bool = True) -> None:
        self._button: dict = {}

        self.buttonType: str = 'web_url'
        set_if_exists(self, '_title', text, maxLen=self.TITLE_CHAR_LIMIT)
        set_if_exists(self, '_url', url)
        if messengerExtensions:
            self._messengerExtensions: bool = True
            set_if_exists(self, '_fallbackUrl', fallbackUrl)
        set_if_exists(self,
                      '_webviewHeightRatio', webviewHeightRatio, types=self.WEB_VIEW_HEIGHT_RATIOS)
        if not webviewShareButton:
            self._webviewShareButton: str = 'hide'

    def build(self) -> dict:
        if not hasattr(self, '_button'):
            self._button: dict = {}
            self._button['type'] = self.buttonType
            self._button['title'] = getattr(self, '_title')
            self._button['url'] = getattr(self, '_url')
            if self._messengerExtensions:
                self._button['messenger_extensions'] = \
                    self._messengerExtensions
                self._button['fallback_url'] = \
                    getattr(self, '_fallbackUrl')
            if hasattr(self, '_webviewHeightRatio'):
                self._button['webview_height_ratio'] = \
                    getattr(self, '_webviewHeightRatio')
            if hasattr(self, '_webviewShareButton'):
                self._button['webview_share_button'] = \
                    self._webviewShareButton
        return self._button


# DONE
class PostbackButton(Button):
    def __init__(self, text: str, postbackData: str) -> None:
        self.buttonType: str = 'postback'
        set_if_exists(self,
                      '_title', text, maxLen=self.BUTTON_TITLE_CHAR_LIMIT)
        self._payload: str = postbackData

    def build(self) -> dict:
        if not hasattr(self, '_button'):
            self._button: dict = {
                'type': 'postback',
                'title': getattr(self, '_title'),
                'payload': self._payload}
        return self._button


# DONE
class ShareButton(Button):
    def __init__(self, template=None) -> None:
        self.buttonType = 'element_share'
        if template:
            # Defined here to avoid circular dependencies
            from bartbot.send.attachment import ShareTemplate
            if isinstance(template, ShareTemplate):
                self._shareTemplate = template
            else:
                raise ValueError(
                    "Must pass in a ShareTemplate into ShareButton template")
            if self._shareTemplate.templateType != 'generic':
                raise ValueError("Share button template must be generic")

    def build(self) -> dict:
        if not hasattr(self, '_button'):
            self._button: dict = {}
            self._button['type'] = self.buttonType
            if hasattr(self, '_shareTemplate'):
                self._button['share_contents'] = {
                    'attachment': self._shareTemplate.build()}
        return self._button

# me: "shaq, how do you feel about kobe bryant shaving his mustache?"
# shaq: "have you ever cut your eyebrows? or i mean just one; you have like one red one"
# someone else that i knew: "yeah right there"
# me: "oh yeah, i can see it"
# * shaq plucks the red eyebrow *
# shaq: "there it is."
# me: "woah this is a weird eyebrow. it has seeds in it!"
# * looks inside red eyebrow to find tomato seeds inside *
# ** wakes up **


# DONE
class CallButton(Button):
    def __init__(self, text: str, phoneNumber: str) -> None:
        """
        Create a button that calls the phone number provided. This
            function doesn't validifiy the given phone number.
        NOTE: phoneNumber must contain a '+' followed by a valid
            country code.
        """
        self.buttonType: str = 'phone_number'
        set_if_exists(self, '_title', text, self.BUTTON_TITLE_CHAR_LIMIT)
        set_if_exists(self, '_payload', phoneNumber, prefix='+')

    def build(self) -> dict:
        if not hasattr(self, '_button'):
            self._button: dict = {
                'type': self.buttonType,
                'title': getattr(self, '_title'),
                'payload': getattr(self, '_payload')}
        return self._button
