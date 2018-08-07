"""Bartbot

Run this program roughly every two weeks or when necessary to keep station list up to date. Program contacts BART API and writes JSON/Python Dict object to file `resources/stationABbrToStationName.json` for other programs to read."""

__author__ = 'Anthony W. Ho'

from json import JSONEncoder

import __future__
import os
import requests

import passingStatus
import apiInfo

# Public API key - this code will not be run very often. 
KEY = apiInfo.BART_PUBLIC
# TODO: Generalize this path to make it easier to find later in project
TARGET = os.path.join(os.path.dirname(__file__), "..", "resources", "stationAbbrToStationName.json")

def updateStations():
  print('Updating stations...')
  urlEndpoint = apiInfo.BART_API_URL + 'stn.aspx'
  payload = {'cmd': 'stns', 'key': KEY, 'json': 'y'}

  try:
    r = requests.get(urlEndpoint, payload)
  except Exception as e:
    print(e)
    print('Error: Could not establish connection to {}.'.format(urlEndpoint))
    return False
  
  content = r.content.decode('utf-8')

  if not passingStatus.check(r):
    print('Error: Could not update stations.')
    return False
  elif r.status_code == 200:
    if '<error>' in content:
      print('Response content: {}'.format(content))
      print('Error: Could not update stations.')
      return False


  j = r.json()
  abbrToName = {}

  for s in j['root']['stations']['station']:
    abbrToName[s['abbr']] = s['name']

  nJson = JSONEncoder().encode(abbrToName)    
  
  with open(TARGET, 'w') as f:
    try:
      f.write(nJson)
    except Exception as e:
      print(e)
      print("Error: Could not update stations - could not write to file.")
    else:
      print("Stations updated.")
  
  return True


if __name__ == "__main__":
  updateStations()