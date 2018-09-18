import bartbot
from bartbot.utils.urls import (AWS_WEBHOOK, LOCALHOST, MESSAGES_API)
from bartbot.utils.phrases.emojis import (emojis, print_all_emojis)


use_localhost:bool = True
test_url:str = LOCALHOST if use_localhost else AWS_WEBHOOK

