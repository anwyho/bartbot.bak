from bartbot.utils.phrases.emojis import emojis

locale = 'en_US'

from typing import (List)


attachment: List[str] = [
    f"Ooh attachment! I'm starting to get a little attached to you too {emojis['smiling_face_with_smiling_eyes']}",
    f"Ooh! For me? {emojis['face_with_open_mouth']}",
    f"Wow!",
    f"Hmm... {emojis['face_with_raised_eyebrow']} I don't quite know what to do with this.",
    f"Hello there. {emojis['beaming_face_with_smiling_eyes']}",
    f"Whoa what is that?",
    f"Cool!",
]

attachmentWName: List[str] = [
    f"Ooh attachment! I'm starting to get a little attached to you too {{firstName}} {emojis['smiling_face_with_smiling_eyes']}",
    f"Oh thanks {{firstName}}!",
]
