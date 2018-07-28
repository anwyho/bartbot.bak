def check(statusCode):
  if statusCode >= 500:
    print('Error {0}: Server Error'.format(statusCode))
    return False
  elif statusCode == 404:
    print('Error {0}: URL not found: [{1}]'.format(statusCode,api_url))
    return False  
  elif statusCode == 401:
    print('Error {0}: Authentication Failed'.format(statusCode))
    return False
  elif statusCode == 400:
    print('Error {0}: Bad Request'.format(statusCode))
    return False
  elif statusCode >= 300:
    print('Error {0}: Unexpected Redirect'.format(statusCode))
    return False
  elif statusCode != 200:
    print('Unexpected Error: [HTTP {0}]: Content: {1}'.format(statusCode, response.content))
    return False
  return True
