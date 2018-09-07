from . import keys


# URLs
GRAPH_API: str = 'https://graph.facebook.com/'
GRAPH_VER: str = '2.6'
MESSENGER_PLATFORM: str = GRAPH_API+f'v{GRAPH_VER}/me/'
AUTH: str = f'access_token={keys.FB_PAGE_ACCESS}' + \
    f'&appsecret_proof={keys.gen_app_secret_proof()}'

MESSAGES_API: str = MESSENGER_PLATFORM+'messages?'+AUTH
MESSAGE_ATTACHMENTS_API: str = \
    MESSENGER_PLATFORM+'message_attachments?'+AUTH
MESSENGER_PROFILE_API: str = \
    MESSENGER_PLATFORM+'messenger_profile?'+AUTH
MESSENGER_USER_API: str = GRAPH_API+'{fbId}?'+AUTH

# Testing
LOCALHOST = "https://localhost:5000/webhook?"
AWS_WEBHOOK = \
    "https://ick416py79.execute-api.us-west-1.amazonaws.com/dev/webhook?"
