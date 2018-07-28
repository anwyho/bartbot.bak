def check(response):
  if response.status_code >= 500:
    print('Error {0}: Server Error'.format(response.status_code))
    return False
  elif response.status_code == 404:
    print('Error {0}: URL not found: [{1}]'.format(response.status_code,response.url))
    return False  
  elif response.status_code == 401:
    print('Error {0}: Authentication Failed'.format(response.status_code))
    return False
  elif response.status_code == 400:
    print('Error {0}: Bad Request'.format(response.status_code))
    return False
  elif response.status_code >= 300:
    print('Error {0}: Unexpected Redirect'.format(response.status_code))
    return False
  elif response.status_code != 200:
    print('Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
    return False
  return True
