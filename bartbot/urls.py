from . import keys as k


# URLs
GRAPH_API: str = 'https://graph.facebook.com/'
MESSENGER_PLATFORM: str = GRAPH_API+'v2.6/me/'
AUTH: str = 'access_token={token}&appsecret_proof={proof}'.format(
    token=k.FB_PAGE_ACCESS,
    proof=k.gen_app_secret_proof())
    
MESSAGES_URL: str = MESSENGER_PLATFORM+'messages?'+AUTH