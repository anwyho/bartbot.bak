#  _                _   _           _
# | |__   __ _ _ __| |_| |__   ___ | |_
# | '_ \ / _` | '__| __| '_ \ / _ \| __|
# | |_) | (_| | |  | |_| |_) | (_) | |_
# |_.__/ \__,_|_|   \__|_.__/ \___/ \__|
# Get all your BART info from your Messenger app!

from ..emojis import emojis

# NOTE:
# 1. Each string should be an f-string
# 2. Options should be double-bracketed to escape f-string
# 3. Emojis should be single-bracketed to be evaluated
# 4. Ideally, there should be no whitespace on the outsides,
#   but str.strip() is called anyway
# 5. Call bartbot.utils.phrases.emojis.print_all_emojis() for easily copy-paste

locale = "en_US"

phrases = {
    'attachment': [
        f"Ooh attachment! I'm starting to get a little attached to you too {{opt[fn]}} {emojis['smiling_face_with_smiling_eyes']}",
        f"Ooh attachment! I'm starting to get a little attached to you too {emojis['smiling_face_with_smiling_eyes']}",
        f"Ooh! For me? {emojis['face_with_open_mouth']}",
        f"Wow!",
        f"Hmm... {emojis['face_with_raised_eyebrow']} I don't quite know what to do with this.",
        f"Hello there. {emojis['beaming_face_with_smiling_eyes']}",
        f"Whoa what is that?",
        f"Cool!",
    ],
    'bye': [
        f"See ya later!",
        f"See ya later {{opt[fn]}}!",
        f"Adios!",
        f"Bye bye!",
        f"Zai jian!",
        f"Take care.",
        f"Love you!",
        f"BART safe!",
        f"Bye!",
        f"Bye {{opt[fn]}}!",
        f"Tootles!",
        f"TTFN",
        f"TTYL",
        f"TTYL {{opt[fn]}}!",
        f"Later!",
        f"Until next time!",
        f"Until next time, {{opt[fn]}}!",
    ],
    # CTA usually follows hello.
    # NOTE: No {opt}s because name would"ve already been stated.
    # TODO: Seaprate the ones with names into a different category
    'cta': [
        f"Where are you headed?",
        f"Where are you headed today?",
        f"Where would you like to go?",
        f"Where would you like to go today?",
        f"Where are you off to?",
        f"Where are you off to today?",
        f"Where to?",
        f"Where ya headed?",
        f"Where ya headed today?",
        f"Headed anywhere?",
    ],
    'delivery': [
        f"Here it is!",
        f"Here you go!",
        f"Here ya go {{opt[fn]}}!",
        f"Here ya go!",
        f"There ya go!",
        f"Special delivery!",
        f"Special delivery, for {{opt[fn]}}",
    ],
    'hello': [
        f"Greetings.",
        f"Hello there.",
        f"Sup!",
        f"Sup {{opt[fn]}}!",
        f"Hello from the other side!",
        f"Good day!",
        f"Good day, {{opt[fn]}}!",
        f"Good {{opt[time_of_day]}}!",
        f"Good {{opt[time_of_day]}} {{opt[fn]}}!",
        f"Hi there!",
        f"Hello!",
        f"Hello {{opt[fn]}}!",
        f"Hi!",
        f"Hi {{opt[fn]}}!",
        f"Hey, didn't see ya there!",
    ],
    'sorry': [
        f"Sorry about that!",
        f"Oops! {emojis['shushing_face']}",
        f"Oh no. {emojis['face_screaming_in_fear']}",
        f"Hmm...",
        f"Darn. {emojis['crying_face']}",
        f"Shucks. {emojis['crying_face']}",
        f"That's embarrassing... {emojis['grinning_face_with_sweat']}",
        f"Aiya!",
        f"Whoops! {emojis['dizzy_face']}",
        f"My bad! {emojis['grinning_face_with_sweat']}",
    ],
    'thanks': [
        f"Thanks! {emojis['smiling_face_with_smiling_eyes']}",
        f"Thanks! {emojis['thumbs_up']}",
        f"Thanks!",
        f"Thankya!",
        f"Wow thanks!",
        f"tysm!",
        f"TY!",
        f"Xie xie!",
    ],
    'time-specific emoji': [  # How do I even code this section
        f"{emojis['sleeping_face']}",
    ],
    'wait': [
        f"One moment please...",
        f"One sec...",
        f"BRB!",
        f"Hold up...",
        f"Lemme get something...",
        f"Just a moment!",
        f"One moment {{opt[fn]}}",
        f"One sec {{opt[fn]}}...",
        f"Just a moment {{opt[fn]}}!",
    ],
    'yw': [
        f"You're welcome!",
        f"Have a great {{opt[time_of_day_w_night]}}!",
        f"Anytime!",
        f"Yeah, no problem!",
        f"Safe travels!",
    ],
}
