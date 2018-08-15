from __future__ import print_function

import boto3
import botocore
import json
import requests

from json import JSONDecoder

import apiInfo

VERIFY_TOKEN = "my_awesome_token";
PAGE_ACCESS_TOKEN = apiInfo.FB_PAGE_ACCESS_KEY

def processMessage(event, context):
  print("Received event: " + json.dumps(event, indent=2))

  # GET request
  # TODO

  # POST request
  # TODO

  return event['key1']  # Echo back the first key value
  raise Exception('Something went wrong')






