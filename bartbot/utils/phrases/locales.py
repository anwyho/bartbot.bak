"""The locales module keeps a list of all supported locales and returns errors on import failures."""

import importlib
import logging

from types import ModuleType
from typing import (Tuple, Optional)


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
    "zh_cn" : "zh_CN",
    "zh_hk" : "zh_HK_TW",
    "zh_tw" : "zh_HK_TW",
}

def import_locale_module(locale:str=DEFAULT_LOCALE) -> Tuple[ModuleType,str]:
    locale = locale.lower()
    if locale in SUPPORTED_LOCALES:
        logging.info(f"Importing locale {locale}")
        return importlib.import_module(
                '.phrases_'+SUPPORTED_LOCALES[locale], 
                package="bartbot.utils.phrases."+
                    SUPPORTED_LOCALES[locale]), locale
    else:
        if locale == DEFAULT_LOCALE:
            logging.error("Couldn't find default locale. Probably unset it or dereferenced it in `bartbot/utils/phrases/locales.py. Fix ASAP!")
            raise ModuleNotFoundError(f"Support for default locale is not implemented. Please implement default locale.")
        else: 
            raise KeyError(f"Locale {locale} is not in list of supported locales")
