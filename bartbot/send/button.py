
import json
import logging

from abc import (ABC, abstractmethod)
from typing import (List, Optional)

# # Defined below to avoid circular dependencies
# from bartbot.send.template import Template


class Button(ABC):
    BUTTON_TYPES: List[Optional[str]] = [
        'web_url',
        'postback',
        'element_share',
        'phone_number',
        None]

    MAX_BUTTON_TITLE_CHAR_LENGTH = 20

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
                f"Attempted to make unsupported button type.{buttonType}.")

    @abstractmethod
    def build(self) -> dict:
        """Builds itself as a dict to be placed into a built template"""
        pass


class UrlButton(Button):

    WEB_VIEW_HEIGHT_RATIOS = ['compact', 'tall', 'full']

    def __init__(self,
                 title: str,
                 url: str,
                 webViewHeightRatio: Optional[str] = None,
                 messengerExtensions: bool = False,
                 fallbackUrl: Optional[str] = None,
                 webViewShareButton: Optional[str] = None) -> None:
        self.buttonType = 'web_url'
        if len(title) > 20:
            logging.warning(
                f"Title message {title} is too long. Title must be {self.MAX_BUTTON_TITLE_CHAR_LENGTH} characters or less and has been truncated.")
        self._title = title[:self.MAX_BUTTON_TITLE_CHAR_LENGTH]
        self._url = url
        if webViewHeightRatio and webViewHeightRatio in self.WEB_VIEW_HEIGHT_RATIOS:
            self._webviewHeightRatio = webViewHeightRatio
        if messengerExtensions:
            self._messengerExtensions = True
            self._fallbackUrl = fallbackUrl
        if webViewShareButton:
            self._webviewShareButton = webViewShareButton

    def build(self) -> dict:
        data: dict = {}
        data['type'] = self.buttonType
        data['title'] = self._title
        data['url'] = self._url
        if hasattr(self, '_webviewHeightRatio'):
            data['webview_height_ratio'] = self._webviewHeightRatio
        if self._messengerExtensions:
            data['messenger_extensions'] = self._messengerExtensions
            data['fallback_url'] = self._fallbackUrl
        if hasattr(self, '_webviewShareButton')
        data['webview_share_button'] = self._webviewShareButton
        return data


class PostbackButton(Button):
    def __init__(self, text: str, postbackData: str) -> None:
        self.buttonType = 'postback'
        self._title = text
        self._payload = postbackData

    def build(self) -> dict:
        return {'type': 'postback',
                'title': self._title,
                'payload': self._payload}


class ShareButton(Button):
    def __init__(self, **kwargs) -> None:
        self.buttonType = 'element_share'
        from bartbot.send.template import Template
        self._shareTemplate = Template.make_template(
            templateType='share', **kwargs)
        if self._shareTemplate.templateType != 'generic':
            raise ValueError("Share button template must be generic")

    def build(self) -> dict:
        return {'type': self.buttonType,
                'share_contents': {'attachment':
                                   {self._shareTemplate.build()}}}


class CallButton(Button):
    def __init__(self, text: str, phoneNumber: str) -> None:
        """
        Create a button that calls the phone number provided. This function doesn't validifiy the given phone number.
        phoneNumber must contain a '+' followed by a valid country code.
        """
        self.buttonType: str = 'phone_number'
        self._title: str = text
        self._payload: str = phoneNumber
        if phoneNumber.lstrip()[0] != '+':
            raise ValueError(
                "Expected phone number {phoneNumber} to contain '+' followed by a country code.")

    def build(self) -> dict:
        return {'type': self.buttonType,
                'title': self._title,
                'payload': self._payload}
