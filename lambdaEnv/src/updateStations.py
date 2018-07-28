from json import JSONEncoder
import os
import requests

KEY = 'ZSBD-57UA-9TVT-DWE9'
TARGET = os.path.join(os.path.dirname(__file__), "..", "resources", "stationAbbrToStationName.json")

def updateStations():
  print('Updating stations...')
  urlEndpoint = 'http://api.bart.gov/api/stn.aspx'
  payload = {'cmd': 'stns', 'key': KEY, 'json': 'y'}

  r = requests.get(urlEndpoint, payload)
  print(r.url)
  print(r.status_code)
  if (r.status_code == 200):
    with open(TARGET, 'w') as f:
      j = r.json()
      abbrToName = {}
      for s in j['root']['stations']['station']:
        abbrToName[s['abbr']] = s['name']
      nJson = JSONEncoder().encode(abbrToName)
      print(nJson)
      f.write(nJson)
  else: 
    raise Exception('Request for {url} responded with error {err}'
        .format(url=urlEndpoint, err=r.status_code))


if __name__ == "__main__":
  updateStations()