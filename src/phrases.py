# from __future__ import print_function
# from __future__ import unicode_literals

import random as r
import time

def get_phrase(*sentences):
    """Constructs randomized sentences of phrase lists"""
    return " ".join(map(r.choice,sentences))


def time_of_day(night=False):
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

hello = [
    'Greetings.',
    'Hello there.',
    'Sup!',
    'Sup {fn}!'
    'Hello from the other side!',
    'Good day!', 
    'Good day, {fn}!',
    'Good {time}!'.format(time=time_of_day()),
    'Hi there!',
    'Hello!',
    'Hello {fn}!',
    'Hi!',
    'Hi {fn}!',
    ]
cta = [
    'Where are you headed?',
    'Where are you headed today?',
    'Where would you like to go?',
    'Where would you like to go today?',
    'Where are you off to?',
    'Where are you off to today?',
    'Where to?',
    'Where ya headed?',
    'Where ya headed today?',
    ]
yw = [
    'You\'re welcome!',
    'Have a great {time}!'.format(
        time=time_of_day(night=True)),
    'Anytime!',
    'Yeah, no problem!',
    'Safe travels!',
    ]
bye = [
    'See ya later!',
    'See ya later {fn}!',
    'Adios!',
    'Bye bye!',
    'Zai jian!',
    'Take care.',
    'Love you!',
    'BART safe!',
    'Bye!',
    'Bye {fn}!'
    'Tootles!',
    'TTFN',
    'TTYL',
    'TTYL {fn}!',
    'Later!',
    'Until next time!',
    'Until next time, {fn}!',
    'Have a great time!',
    'Have a great time {fn}!',
    ]
delivery = [
    'Here it is!',
    'Here you go!',
    'Here ya go!',
    'There ya go!',
    'Here ya go!',
    'Special delivery!',
    'Special delivery, for {fn}'
]



if __name__ == '__main__':
    print('Phrases demonstration:')
    print(get_phrase(hello,cta))
    print(get_phrase(yw,bye))