# Phrase lists

from ..emoji import emojis
# TODO: More emojis
# TODO: Better support for {opt} (maybe in .format() pass in opt dict)

phrases = {
    'attachment' : [
        f"Ooh attachment! I'm starting to get a little attached to you too {{opt['fn']}} {emojis['smiling_face_with_smiling_eyes']}",
        "Ooh! For me?",
        "Wow!",
        "Hmm... I don't quite know what to do with this.",
        "Hello there.",
        "Whoa what is that?",
        "Cool!",
        ],
    'bye' : [
        "See ya later!",
        "See ya later {opt['fn']}!",
        "Adios!",
        "Bye bye!",
        "Zai jian!",
        "Take care.",
        "Love you!",
        "BART safe!",
        "Bye!",
        "Bye {opt['fn']}!",
        "Tootles!",
        "TTFN",
        "TTYL",
        "TTYL {opt['fn']}!",
        "Later!",
        "Until next time!",
        "Until next time, {opt['fn']}!",
        ],
    # CTA usually follows hello. 
    # NOTE: No {opt}s because name would"ve already been stated.
    'cta' : [
        "Where are you headed?",
        "Where are you headed today?",
        "Where would you like to go?",
        "Where would you like to go today?",
        "Where are you off to?",
        "Where are you off to today?",
        "Where to?",
        "Where ya headed?",
        "Where ya headed today?",
        ],
    'delivery' : [
        "Here it is!",
        "Here it is, {opt['fn']}!",
        "Here you go!",
        "Here ya go {opt['fn']}!",
        "Here ya go!",
        "There ya go!",
        "Special delivery!",
        "Special delivery, for {opt['fn']}",
        ],
    'hello' : [
        "Greetings.",
        "Hello there.",
        "Sup!",
        "Sup {opt['fn']}!",
        "Hello from the other side!",
        "Good day!", 
        "Good day, {opt['fn']}!",
        "Good {opt['time_of_day']}!",
        "Good {opt['time_of_day']} {opt['fn']}!",
        "Hi there!",
        "Hello!",
        "Hello {opt['fn']}!",
        "Hi!",
        "Hi {opt['fn']}!",
        "Hey, didn't see ya there!",
        ],
    'sorry' : [
        "Sorry about that!",
        "Oops!",
        "Oh no!",
        "Hmm...",
        "Darn.",
        "Shucks.",
        "That's embarrassing...",
        "Aiya!",
        "Whoops!",
        "My bad!",
        ],
    'thanks' : [
        "Thanks!",
        "Thankya!",
        "Wow thanks!",
        "tysm!",
        "TY!",
        "Xie xie!",
        ],
    'yw' : [
        "You're welcome!",
        "Have a great {opt['time_of_day_w_night']}!",
        "Anytime!",
        "Yeah, no problem!",
        "Safe travels!",
        ],
}