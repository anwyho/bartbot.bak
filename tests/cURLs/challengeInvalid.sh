curl -X GET "localhost:5000/webhook?hub.mode=subscribe&hub.verify_token=invalid_token&hub.challenge=challenge_should_not_be_accepted"

# curl -X GET "https://ick416py79.execute-api.us-west-1.amazonaws.com/dev/webhook?hub.mode=subscribe&hub.verify_token=OF_MY_APPRECIATION&hub.challenge=challenge_should_not_be_accepted"