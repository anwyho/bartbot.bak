"""
The locales module keeps a list of all supported locales and returns
    errors on import failures.
"""

import importlib
import logging

from types import ModuleType
from typing import (Tuple, Optional)  # noqa: F401

from .supported_locales import (DEFAULT_LOCALE, SUPPORTED_LOCALES)

PROJECT_NAME = 'bartbot'


def import_locale_module(locale: str=DEFAULT_LOCALE) -> Tuple[ModuleType, str]:
    """
    Import a locale-specific module of given locale in compose.utils.phrases.*
    """
    locale = locale.lower()
    if locale in SUPPORTED_LOCALES:
        logging.info(f"Importing locale {locale}")
        return importlib.import_module(
            f".{PROJECT_NAME}_{SUPPORTED_LOCALES[locale]}",
            package=f"compose.utils.phrases"), locale

    else:
        if locale == DEFAULT_LOCALE:
            logging.error(
                "Couldn't find default locale. Probably unset it or "
                "dereferenced it in `compose/utils/phrases/locales.py. "
                "Fix ASAP!")
            raise ModuleNotFoundError(
                "Support for default locale is not implemented. Make sure "
                "the default locale is set or implemented.")
        else:
            raise KeyError(
                f"Locale {locale} is not in list of supported locales")
