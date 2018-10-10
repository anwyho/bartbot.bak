
import json
import logging

from abc import (ABC, abstractmethod)
from typing import (List, Optional)

from bartbot.send.button import Button


class Template(ABC):

    TEMPLATE_TYPES: List[Optional[str]] = [
        'generic',
        'button',
        'list',
        'media',
        # 'receipt',  # not currently supported
        'share',
        None]

    def __init__(self, templateType: str, **kwargs) -> None:
        if templateType in self.TEMPLATE_TYPES:
            self.templateType: str = templateType
        else:
            logging.warning(
                f"Attempted to make unsupported template type {templateType}.")

    @classmethod
    def make_template(cls, templateType: str, **kwargs):
        if templateType == 'generic':
            return GenericTemplate(**kwargs)
        elif templateType == 'button':
            return ButtonTemplate(**kwargs)
        elif templateType == 'list':
            return ListTemplate(**kwargs)
        elif templateType == 'media':
            return MediaTemplate(**kwargs)
        elif templateType == 'share':
            return ShareTemplate(**kwargs)
        else:
            # TODO: ValueError

    @abstractmethod
    def build(self) -> dict:
        return {
            'type': 'template',
        }


class GenericTemplate(Template):

    # TODO: Make more constants to check

    class GenericElement:
        def __init__(self,
                     url: str,
                     webViewHeightRatio: Optional[str] = None,
                     messengerExtensions: bool = False,
                     fallbackUrl: Optional[str] = None,
                     webViewShareButton: Optional[str] = None) -> None:
            self._url = url
            if webViewHeightRatio:
                self.webViewHeightRatio = webViewHeightRatio
            if messengerExtensions:
                self.messengerExtensions = True
                self.fallbackUrl = fallbackUrl
            if webViewShareButton:
                self.webViewHeightRatio = webViewHeightRatio

        def build(self) -> dict:
            data: dict = {}
            data['url'] = self._url
            if hasattr(self, '_webviewHeightRatio'):
                data['webview_height_ratio'] = self._webviewHeightRatio
            if self._messengerExtensions:
                data['messenger_extensions'] = self._messengerExtensions
                data['fallback_url'] = self._fallbackUrl
            if hasattr(self, '_webviewShareButton')
            data['webview_share_button'] = self._webviewShareButton
            return data

    def __init__(self):
        self.templateType: str = 'generic'
        self._elements: list = []  # TODO: Initialize elements

    def build(self) -> dict:
        elements = [e.build() for e in self._elements]

        payload: dict = {
            'template_type': 'generic',
            'elements': elements}
        super().build()['payload'] = payload


class ButtonTemplate(Template):
    class ButtonElement:
        def __init__(self):
            pass

    def __init__(self):
        pass

    def build(self) -> dict:
        pass


class ListTemplate(Template):
    # TODO: Make ListElement
    def __init__(self):
        pass

    def build(self) -> dict:
        pass


class MediaTemplate(Template):
    # TODO: Make MediaTemplate
    def __init__(self):
        pass

    def build(self) -> dict:
        pass


class ShareTemplate(Template):
    # TODO: Connect GenericElement
    def __init__(self):
        pass

    def build(self) -> dict:
        pass
