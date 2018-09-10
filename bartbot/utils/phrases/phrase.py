# TODO: Ambiguous filenames? Maybe change to PhraseFactory or something

import logging
import random as r
import time

from typing import (List, Tuple, Union)

from .locales import (DEFAULT_LOCALE, import_locale_package)

currentLocale = None
localeModule = None

def set_locale(newLocale:str) -> bool:
    # TODO: Function docstring
    
    # Check if current locale already exists
    global currentLocale
    global localeModule
    if localeModule is not None and newLocale is currentLocale: 
        logging.info(f"New locale {newLocale} and current locale {currentLocale} are the same")
        return localeModule
    elif newLocale is None: 
        newLocale = DEFAULT_LOCALE
    
    # Tries to import locale package
    logging.info(f"Setting locale to {newLocale}")
    newLocale = newLocale.lower()
    try: 
        
        localeModule = import_locale_package(newLocale)
    except ImportError as e:
        logging.error(f"Failed to import package for locale {newLocale}. Error: {e}")
        return None
    except KeyError as e:
        logging.error(f"Failed to import package for locale {newLocale}. Error: {e}")
        return None
    
    currentLocale = newLocale
    return localeModule

    
# HACK: This will hang if :
    # no opt is given or `opt = '{opt}'` AND
    # the phrases in localeModule.phrases all contain `{opt}`
        # it will also take more runtime if almost every string 
        #   contains `{opt}``
# TODO: Improve performance. Hanging can take up to 5 seconds...
# TODO: Check that each typeOfSentence exists in localeModule.phrases
    # ONERROR: Fail silently, remove type from typeOfSentence
    #   Remember to logging.debug
def get_phrase(
        *typesOfPhrases:str, 
        opt:str='{opt}', 
        locale:str=DEFAULT_LOCALE) -> str:
    """Constructs randomized sentences of types of phrases"""

    set_locale(locale) 
    resp = '{opt}'


    while '{opt}' in resp: 
        # Maps random choice on each phrase type depending on locale and 
        #   joins them to make a phrase
        resp = ' '.join(map(r.choice,[localeModule.phrases[type] for type in typesOfPhrases])).format(
            opt=opt,
            time_of_day=time_of_day(night=False),
            time_of_day_night=time_of_day(night=True))
    return resp


# TODO: Connect this to localeModule.times
def time_of_day(night:bool=False) -> str:
    """Returns signifier for the time of day"""
    global localeModule
    global currentLocale
    hour = time.localtime().tm_hour 

    if currentLocale is "en_us":
        if night and (hour > 21 or hour <= 4):
            return "night"
        elif hour > 16:
            return "evening"
        elif hour > 11:
            return "afternoon"
        elif hour > 4:
            if r.randint(0,3) != 0:
                return "morning"
            else: 
                return "day"
        else:
            return "night"
    elif currentLocale is "ja_jp":
        pass
    elif currentLocale is "es_la":
        pass
    elif currentLocale is "zh_cn" or \
         currentLocale is "zh_hk" or \
         currentLocale is "zh_tw":
        pass
    raise NotImplementedError(f"Retrieving times of day for locale {currentLocale} is not currently supported.")

# # Sample of what localeModule.times would look like
# times = {
#     4 : "morning",
#     12 : "afternoon",
#     16 : "evening",
#     21 : "night",
# }

    













if __name__ == '__main__':
    print("Phrases demonstration:")
    print(get_phrase('hello','cta'))
    print(get_phrase('yw','bye'))
