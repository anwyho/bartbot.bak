# TODO: Ambiguous filenames? Maybe change to PhraseFactory or something

import logging
import random as r
import time

from typing import (List, Tuple, Union)

from .locales import (DEFAULT_LOCALE, import_locale_package)

currentLocale = None
localePkg = None

def set_locale(newLocale:str) -> bool:
    # TODO: Function docstring
    
    # Check if current locale already exists
    global currentLocale
    global localePkg
    if localePkg is not None and newLocale is currentLocale: 
        logging.info(f"New locale {newLocale} and current locale {currentLocale} are the same")
        return localePkg
    elif newLocale is None: 
        newLocale = DEFAULT_LOCALE
    
    # Tries to import locale package
    logging.info(f"Setting locale to {newLocale}")
    newLocale = newLocale.lower()
    try: 
        
        localePkg = import_locale_package(newLocale)
    except ImportError as e:
        logging.error(f"Failed to import package for locale {newLocale}. Error: {e}")
        return None
    except KeyError as e:
        logging.error(f"Failed to import package for locale {newLocale}. Error: {e}")
        return None
    
    currentLocale = newLocale
    return localePkg

    
# HACK: This will hang if :
    # no opt is given or `opt = '{opt}'` AND
    # the phrases in localePkg.phrases all contain `{opt}`
        # it will also take more runtime if almost every string 
        #   contains `{opt}``
# TODO: Improve performance. Hanging can take up to 5 seconds...
# TODO: Check that each typeOfSentence exists in localePkg.phrases
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
        resp = ' '.join(map(r.choice,[localePkg.phrases[type] for type in typesOfPhrases])).format(
            opt=opt,
            time_of_day=time_of_day(night=False),
            time_of_day_night=time_of_day(night=True))
    return resp


# TODO: Connect this to localePkg.times
def time_of_day(night:bool=False) -> str:
    """Returns signifier for the time of day"""
    global localePkg

    hour = time.localtime().tm_hour 
    if night and (hour > 21 or hour <= 4):
        return "night"
    elif hour > 16:
        return "evening"
    elif hour > 11:
        return "afternoon"
    elif hour > 4 and r.randint(0,3) != 0:
        return "morning"
    else :
        return "day"



    













if __name__ == '__main__':
    print("Phrases demonstration:")
    print(get_phrase('hello','cta'))
    print(get_phrase('yw','bye'))
