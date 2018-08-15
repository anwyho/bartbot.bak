"""Bartbot

Simple function to parse response status of a request. Adopted from https://www.digitalocean.com/community/tutorials/how-to-use-web-apis-in-python-3"""

from __future__ import print_function

__author__ = "Anthony W. Ho"

def check(response):
  """Returns True in the case of a passing response code. Returns false and prints out the error in the case of a bad response code."""

  isPassing = True

  if response.status_code >= 500:
    print('Error {0}: Server Error'.format(response.status_code))
    isPassing = False
  elif response.status_code == 404:
    print('Error {0}: URL not found: [{1}]'.format(response.status_code,response.url))
    isPassing = False  
  elif response.status_code == 401:
    print('Error {0}: Authentication Failed'.format(response.status_code))
    isPassing = False
  elif response.status_code == 400:
    print('Error {0}: Bad Request'.format(response.status_code))
    isPassing = False
  elif response.status_code >= 300:
    print('Error {0}: Unexpected Redirect'.format(response.status_code))
    isPassing = False
  elif response.status_code != 200:
    print('Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
    isPassing = False

  return isPassing
