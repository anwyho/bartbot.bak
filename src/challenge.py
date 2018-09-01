def process_get(request):
    """
    A webhook that returns a challenge from a Messenger Platform GET challenge
    """
    queryParams = request.args
    verify_token = queryParams['hub.verify_token']
    if verify_token == FB_VERIFY_TOKEN and \
            queryParams['hub.mode'] == 'subscribe':
        return queryParams['hub.challenge']
    else: 
        return 'Invalid Request or Verification Token.'