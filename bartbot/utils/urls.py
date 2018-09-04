from . import keys


# URLs
GRAPH_API: str = 'https://graph.facebook.com/'
MESSENGER_PLATFORM: str = GRAPH_API+'v2.6/me/'
AUTH: str = 'access_token={token}&appsecret_proof={proof}'.format(
    token=keys.FB_PAGE_ACCESS,
    proof=keys.gen_app_secret_proof())
    
MESSAGES_API: str = MESSENGER_PLATFORM+'messages?'+AUTH
MESSAGE_ATTACHMENTS_API: str = MESSENGER_PLATFORM+'message_attachments?'+AUTH
MESSENGER_PROFILE_API: str = MESSENGER_PLATFORM+'messenger_profile?'+AUTH
MESSENGER_USER_API: str = GRAPH_API+'{fbId}?'+AUTH
