"""
The phrase module statically remembers the current locale and provides a facade to the locales, phrases, and emojis modules. It allows the setting of new locales and provides a fault-tolerant interface for phrase generation.
"""

# TODO: Ambiguous filenames? Maybe change to PhraseFactory or something

import logging
import random as r
import time

from types import ModuleType
from typing import (List, Tuple, Optional)

from .locales import (DEFAULT_LOCALE, import_locale_module)


currentLocale = None
phrasesModule = None

# NOTE: This module has been turned into a class and placed in ./__init__.py

# WARNING: The following code is all deprecated.


# DEPRECATED
def set_locale(newLocale: str=None) -> ModuleType:
    """
    Idempotent function that sets locale for the current package. If no locale is given, current locale is set and returned with fallback to default locale.
    Always returns a usable phrases module or raises an error.
    """

    global currentLocale
    global phrasesModule

    if newLocale is None:  # no argument given
        if currentLocale is None:  # no locale set
            return set_locale(DEFAULT_LOCALE)  # set default locale
        else:  # locale is set
            return set_locale(currentLocale)  # set locale
    elif newLocale == currentLocale and phrasesModule is not None:
        logging.info(
            f"New locale {newLocale} and current locale {currentLocale} are the same")
        return phrasesModule  # current phrasesModule is new locale

    logging.info(f"Setting locale to {newLocale}")
    newLocale = newLocale.lower()

    try:
        phrasesModule, currentLocale = import_locale_module(newLocale)
    except ImportError as e:
        logging.warning(
            f"Failed to import package for locale {newLocale}. Error: {e}")
        return import_locale_module()[0]
    except KeyError as e:
        logging.warning(
            f"Failed to import package for locale {newLocale}. Error: {e}")
        return import_locale_module()[0]

    return phrasesModule


# DEPRECATED
# HACK: This will hang if :
    # no opt is given or `opt = '{opt}'` AND
    # the phrases in phrasesModule.phrases all contain `{opt}`
    # it will also take more runtime if almost every string
    #   contains `{opt}``
# TODO: Improve performance. Hanging can take up to 5 seconds...
#   Remove random beyond initial call?
def get_phrase(
        *typesOfPhrases,
        opt: dict={'fn': '{opt[fn]}'},
        locale: str=None) -> str:
    """Constructs randomized sentences of types of phrases"""

    # get_phrase() should use locale temporarily and currentLocale if possible and fallback to DEFAULT_LOCALE
    if locale is not None:  # attempt to load given locale
        locale = locale.lower()
        try:
            curPhrasesModule, _ = import_locale_module(locale)
        except KeyError as e:
            logging.warning(
                "Couldn't import locale {locale}. Using default locale")
            curPhrasesModule, _ = import_locale_module()  # fallback
    elif locale is None:  # no locale given
        global phrasesModule
        if phrasesModule is None:  # no phrases module set
            curPhrasesModule = set_locale()  # attempts to load phrases
        elif phrasesModule is not None:
            curPhrasesModule = phrasesModule

    # Sets dictionary of terms to replace
    resp = '{opt'
    if 'fn' not in opt:
        opt['fn'] = "{opt[fn]}"
    if 'time_of_day_wo_night' not in opt:
        opt['time_of_day_w_night'] = time_of_day(night=True)
    if 'time_of_day' not in opt:
        opt['time_of_day'] = time_of_day(night=False)

    # Loops through choosing phrases until sentence has no more placeholders.
    while '{opt' in resp:
        # Maps random choice on each phrase list type
        #   depending on locale and joins them to make a phrase
        resp = ' '.join(
            [
                r.choice(phrasesMod.phrases[type]).strip()
                if type in phrasesMod.phrases
                else type.strip()
                for type in typesOfPhrases
            ]
        ).format(opt=opt)

    logging.debug(f"Phrase being returned: {resp}")
    return resp

# DEPRECATED
# TODO: Connect this to localeModule.times


def time_of_day(night: bool=False) -> str:
    """Returns signifier for the time of day"""
    global phrasesModule
    global currentLocale
    hour = time.localtime().tm_hour
    if currentLocale == "en_us":
        if night and (hour > 21 or hour <= 4):
            return "night"
        elif hour > 16:
            return "evening"
        elif hour > 11:
            return "afternoon"
        elif hour > 4:
            if r.randint(0, 3) != 0:
                return "morning"
            else:
                return "day"
        else:
            return "night"
    elif currentLocale == "ja_jp":
        pass
    elif currentLocale == "es_la":
        pass
    elif currentLocale == "zh_cn" or \
            currentLocale == "zh_hk" or \
            currentLocale == "zh_tw":
        pass
    raise NotImplementedError(
        f"Retrieving times of day for locale {currentLocale} is not currently supported.")

# # Sample of what localeModule.times would look like
# times = {
#     4 : "morning",
#     12 : "afternoon",
#     16 : "evening",
#     21 : "night",
# }


if __name__ == '__main__':
    print("Phrases demonstration:")
    print(get_phrase('hello', 'cta'))
    print(get_phrase('yw', 'bye'))
