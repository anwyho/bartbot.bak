import importlib
import logging

from types import ModuleType
from typing import (Tuple, Union)


DEFAULT_LOCALE = "en_us"

SUPPORTED_LOCALES:dict = {
    "en_us" : "en_US",
    "en_gb" : "en_US",
    "en_ud" : "en_US",
}

FUTURE_SUPPORTED_LOCALES:dict = {
    "es_la" : "es_LA",
    "ja_jp" : "ja_JP",
    "ja_ks" : "ja_JP",
    "zh_cn" : "zh_CN_HK_TW",
    "zh_hk" : "zh_CN_HK_TW",
    "zh_tw" : "zh_CN_HK_TW",
}

def import_locale_package(locale:str=DEFAULT_LOCALE) -> ModuleType:
    locale = locale.lower()
    if locale in SUPPORTED_LOCALES:
        logging.info(f"Importing locale {locale}")
        return importlib.import_module(
                '.phrase', 
                package="bartbot.utils.phrases."+
                    SUPPORTED_LOCALES[locale])
    else:
        if locale == DEFAULT_LOCALE:
            raise ModuleNotFoundError(f"Support for default locale is not implemented. Please implement default locale.")
        else: 
            raise KeyError(f"Locale {locale} is not in list of supported locales")
