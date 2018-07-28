from json import JSONEncoder
import os
import requests

import passingStatus

KEY = 'ZSBD-57UA-9TVT-DWE9'
TARGET = os.path.join(os.path.dirname(__file__), "..", "resources", "stationAbbrToStationName.json")

def updateStations():
  print('Updating stations...')
  urlEndpoint = 'http://api.bart.gov/api/stn.aspx'
  payload = {'cmd': 'stns', 'key': KEY, 'json': 'y'}

  r = requests.get(urlEndpoint, payload)

  if not passingStatus.check(r.status_code):
    print('Error: Could not update stations.')
    return False
  
  with open(TARGET, 'w') as f:
    j = r.json()
    abbrToName = {}
    for s in j['root']['stations']['station']:
      abbrToName[s['abbr']] = s['name']
    nJson = JSONEncoder().encode(abbrToName)
    print(nJson)
    f.write(nJson)
  
  return True

if __name__ == "__main__":
  updateStations()