import logging
import random as r
import time

from types import ModuleType
from typing import (List, Tuple, Optional)  # noqa: F401

from bartbot.utils.phrases.locales import (
    DEFAULT_LOCALE, import_locale_module)


class Phrase():
    def __init__(self, initialLocale=None):
        self._phraseModule: ModuleType = None
        self._locale: str = initialLocale
        self._set_locale(self._locale)

    @property
    def locale(self) -> str:
        return self._locale

    @locale.setter
    def locale(self, newLocale: Optional[str]) -> None:
        self._set_locale(newLocale)

    def _set_locale(self, newLocale: Optional[str] = None) \
            -> Tuple[ModuleType, str]:
        """
        Idempotent function that sets locale for Phrase class. If no
            locale is given, self._locale is set and returned with
            fallback to default locale.
        Always returns a usable phrases module or raises an error.
        """
        localePkg = None
        if newLocale is None:  # No argument given
            if self._locale is None:  # No locale set
                # Then set default locale
                localePkg = self._set_locale(DEFAULT_LOCALE)
            else:  # Locale set
                # Then set locale to import phrase module
                localePkg = self._set_locale(self._locale)

        # Locale is set and phrase module exists
        elif newLocale == self._locale and \
                self._phraseModule is not None:
            # Then return current phrase module
            localePkg = (self._phraseModule, self._locale)

        else:  # Locale is set but phrase module is None
            # Then import a new phrase module
            self._phraseModule, self._locale = \
                Phrase.safe_locale_import(newLocale)
            localePkg = (self._phraseModule, self._locale)

        return localePkg

    def get_phrase(
            self,
            *typesOfPhrases: str,
            opt: dict={},
            phraseModule: ModuleType=None,
            tempLocale: str=None) -> str:
        """Constructs randomized sentences of types of phrases"""

        phraseModule = self._phraseModule if tempLocale is None else \
            Phrase.safe_locale_import(tempLocale)[0]

        # Provided phrases module has precedence over provided locale
        if phraseModule is None:
            phraseModule = Phrase.safe_locale_import(tempLocale)[0]

        # Sets dictionary of terms to replace
        opt['fn'] = "{opt[fn]}" if 'fn' not in opt else opt['fn']
        opt['time_of_day_w_night'] = self.time_of_day(night=True)
        opt['time_of_day'] = self.time_of_day(night=False)

        # HACK: This will hang if :
        # no opt is given or `opt = '{opt}'` AND
        # the phrases in phraseModule.phrases all contain `{opt}`
        # it will also take more runtime if almost every string
        #   contains `{opt}``
        # TODO: Improve performance. Hanging can take up to 5 seconds...
        #   Remove random beyond initial call?

        # Loops through choosing phrases until sentence has no more
        #   placeholders.
        resp = '{opt'
        while '{opt' in resp:
            # Maps random choice on each phrase list type
            #   depending on locale and joins them to make a phrase
            resp = ' '.join(
                [
                    r.choice(phraseModule.phrases[type]).strip()
                    if type in phraseModule.phrases
                    else type.strip()
                    for type in typesOfPhrases
                ]
            ).format(opt=opt)

        logging.debug(f"Phrase being returned: {resp}")
        return resp

    # TODO: Turn this into a @staticmethod
    # TODO: Connect this to localeModule.times
    # # Sample of what localeModule.times would look like
    # times = {
    #     4 : "morning",
    #     12 : "afternoon",
    #     16 : "evening",
    #     21 : "night",
    # }
    # TODO: Allow tempLocale to be passed in
    def time_of_day(self, night: bool=False) -> str:
        """Returns signifier for the time of day"""
        hour = time.localtime().tm_hour
        if self._locale == "en_us":
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
        elif self._locale == "ja_jp":
            pass
        elif self._locale == "es_la":
            pass
        elif self._locale == "zh_cn" or \
                self._locale == "zh_hk" or \
                self._locale == "zh_tw":
            pass
        raise NotImplementedError(
            f"Retrieving times of day for locale {self._locale} is not "
            "currently supported.")

    @staticmethod
    def safe_locale_import(newLocale: str) -> Tuple[ModuleType, str]:
        """Tries to import a locale with default locale as backup"""
        newLocale = newLocale.lower() if isinstance(newLocale, str) \
            else DEFAULT_LOCALE

        try:
            localeImport = import_locale_module(newLocale)
        except (ImportError, KeyError) as e:
            # Sets default locale as fallback
            localeImport = import_locale_module()
            logging.warning(
                f"Failed to import package for locale {newLocale}. Error: {e}")
        finally:
            return localeImport


if __name__ == '__main__':
    p = Phrase()
    print(p.get_phrase('wait', opt={'fn': 'Anthony'}))
