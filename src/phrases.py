from __future__ import print_function
from __future__ import unicode_literals

import random as r
import time


# Maybe implement some sort of caching and pulling from files? 
    # (Maybe pull from an S3 bucket?)

def time_of_day(night=False):
    """Returns signifier for the time of day"""
    hour = time.localtime().tm_hour 
    if night and hour > 21 or hour <= 4:
        return "night"
    elif hour > 16:
        return "evening"
    elif hour > 11:
        return "afternoon"
    elif hour > 4 and r.randint(0,3) != 0:
        return "morning"
    else :
        return "day"


class PhrasesFactory:
    """Constructs phrases for Bartbot"""

    def __init__(self):
        self.hello = [
            'Greetings.',
            'Hello there.',
            'Sup!',
            'Hello from the other side!',
            'Good day!', 
            'Good {time}!'.format(time=time_of_day()),
            'Hi there!',
            'Hello!',
            'Hi!',
        ]
        self.cta = [
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
        self.yw = [
            'You\'re welcome!',
            'Have a great {time}!'.format(time=time_of_day(night=True)),
            'Anytime!',
            'Yeah, no problem!',
            'Safe travels!',
        ]
        self.bye = [
            'See ya later!',
            'Adios!',
            'Bye bye!',
            'Zai jian!',
            'Take care.',
            # 'Love you!',
            'Bye!',
            'Tootles!',
            'TTFN',
            'TTYL',
            'Later!',
            'Until next time!',
            'Have a great time!',
        ]

    def get_phrase(self, *sentences):
        return " ".join(map(r.choice,sentences))
        

if __name__ == '__main__':
    p = PhrasesFactory()
    print('PhrasesFactory demonstration:')
    print(p.get_phrase(p.hello,p.cta))
    print(p.get_phrase(p.yw,p.bye))