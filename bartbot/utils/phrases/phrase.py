# TODO: Ambiguous filenames? Maybe change to PhraseFactory or something

import logging
import random as r
import time

from typing import (List, Tuple, Union)

from .locales import (DEFAULT_LOCALE, import_locale_package)

currentLocale = None
localeModule = None

def set_locale(newLocale:str=DEFAULT_LOCALE) -> bool:
    # TODO: Function docstring
    
    global currentLocale
    global localeModule
    
    # Check if current locale already exists
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
def get_phrase(
        *typesOfPhrases:str, 
        opt:dict={'fn' : '{opt[fn]}'}, 
        locale:str=DEFAULT_LOCALE) -> str:
    """Constructs randomized sentences of types of phrases"""

    global currentLocale
    global localeModule

    # Check to see if correct locale is installed
    if localeModule is None or currentLocale is not locale:
        logging.info(f"Locale module was not previously set or current locale {currentLocale} is not given locale {locale}. Setting now to locale {locale}.")
        set_locale(locale) 

    resp = '{opt'
    if 'fn' not in opt: 
        opt['fn'] = '{opt[\'fn\']}'
    if 'time_of_day_wo_night' not in opt: 
        opt['time_of_day_w_night'] = time_of_day(night=True)
    if 'time_of_day' not in opt: 
        opt = time_of_day(night=False)

    while '{opt' in resp: 
        # Maps random choice on each phrase list type 
        #   depending on locale and joins them to make a phrase
        resp = ' '.join(
            map(r.choice,
                [localeModule.phrases[type] 
                    if type in localeModule.phrases 
                    else type 
                for type in typesOfPhrases])
            ).format(opt=opt)

    logging.debug(f"Phrase being returned: {resp}")
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
