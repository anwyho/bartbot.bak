import random as r
import time

from typing import List

from .emojis import emojis

def get_phrase(*sentences:List[str], opt:str='{opt}') -> str:
    """Constructs randomized sentences of phrase lists"""
    resp = '{opt}'
    while '{opt}' in resp:
        resp = " ".join(map(r.choice,sentences)).format(opt=opt)  
    return resp


def time_of_day(night:bool=True) -> str:
    """Returns signifier for the time of day"""
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


# Phrase lists
attachments = [
    f"Ooh attachment! I'm starting to get a little attached to you too {{opt}} {emojis['smiling_face_with_smiling_eyes']}",
    "Ooh! For me?",
    "Wow!",
    "Hmm... I don\'t quite know what to do with this.",
    "Hello there.",
    "Whoa what is that?",
    ""
    ]
bye = [
    "See ya later!",
    "See ya later {opt}!",
    "Adios!",
    "Bye bye!",
    "Zai jian!",
    "Take care.",
    "Love you!",
    "BART safe!",
    "Bye!",
    "Bye {opt}!",
    "Tootles!",
    "TTFN",
    "TTYL",
    "TTYL {opt}!",
    "Later!",
    "Until next time!",
    "Until next time, {opt}!",
    ]
# CTA usually follows hello. 
# NOTE: No {opt}s because name would"ve already been stated.
cta = [
    "Where are you headed?",
    "Where are you headed today?",
    "Where would you like to go?",
    "Where would you like to go today?",
    "Where are you off to?",
    "Where are you off to today?",
    "Where to?",
    "Where ya headed?",
    "Where ya headed today?",
    ]
delivery = [
    "Here it is!",
    "Here it is {opt}!",
    "Here you go!",
    "Here ya go {opt}!",
    "Here ya go!",
    "There ya go!",
    "Special delivery!",
    "Special delivery, for {opt}",
    ]
hello = [
    "Greetings.",
    "Hello there.",
    "Sup!",
    "Sup {opt}!",
    "Hello from the other side!",
    "Good day!", 
    "Good day, {opt}!",
    f"Good {time_of_day(night=False)}!",
    f"Good {time_of_day(night=False)} {{opt}}!",
    "Hi there!",
    "Hello!",
    "Hello {opt}!",
    "Hi!",
    "Hi {opt}!",
    "Hey, didn\'t see ya there!"
    ]
sorry = [
    "Sorry about that!",
    "Oops!",
    "Oh no!",
    "Hmm...",
    "Darn.",
    "Shucks.",
    "That\'s embarrassing...",
    "Aiya!",
    "Whoops!",
    ""
    ]
thanks = [
    "Thanks!",
    "Thankya!",
    "Wow thanks!",
    "tysm!",
    "TY!",
    "Xie xie!",
    ]
yw = [
    "You\'re welcome!",
    f"Have a great {time_of_day()}!",
    "Anytime!",
    "Yeah, no problem!",
    "Safe travels!",
    ]







if __name__ == '__main__':
    print("Phrases demonstration:")
    print(get_phrase(hello,cta))
    print(get_phrase(yw,bye))

# TODO: Figure out emoji support