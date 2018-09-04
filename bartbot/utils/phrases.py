# from __future__ import print_function
# from __future__ import unicode_literals

import random as r
import time

def get_phrase(*sentences, opt='{opt}'):
    """Constructs randomized sentences of phrase lists"""
    resp = '{opt}'
    while '{opt}' in resp:
        resp = " ".join(map(r.choice,sentences)).format(opt=opt)  
    return resp


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
    'Sup {opt}!',
    'Hello from the other side!',
    'Good day!', 
    'Good day, {opt}!',
    'Good {time}!'.format(time=time_of_day()),
    'Hi there!',
    'Hello!',
    'Hello {opt}!',
    'Hi!',
    'Hi {opt}!',
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
sorry = [
    'Sorry about that! {opt}',
    'Oops! {opt}',
    'Oh no! {opt}',
    'Hmm... {opt}',
    'Darn. {opt}',
    'Shucks. {opt}',
    'That\'s embarrassing... {opt}',
    'Aiya! {opt}',
    'Whoops! {opt}',
    ''
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
    'See ya later {opt}!',
    'Adios!',
    'Bye bye!',
    'Zai jian!',
    'Take care.',
    'Love you!',
    'BART safe!',
    'Bye!',
    'Bye {opt}!',
    'Tootles!',
    'TTFN',
    'TTYL',
    'TTYL {opt}!',
    'Later!',
    'Until next time!',
    'Until next time, {opt}!',
    ]
delivery = [
    'Here it is!',
    'Here it is {opt}!',
    'Here you go!',
    'Here ya go {opt}!',
    'Here ya go!',
    'There ya go!',
    'Special delivery!',
    'Special delivery, for {opt}',
]



if __name__ == '__main__':
    print('Phrases demonstration:')
    print(get_phrase(hello,cta))
    print(get_phrase(yw,bye))

# TODO: Figure out emoji support