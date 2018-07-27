import requests

KEY = 'ZSBD-57UA-9TVT-DWE9'
RESOURCES = '../resources/stationInfo.txt'

def updateStations():
  print('Updating stations...')
  urlEndpoint = 'http://api.bart.gov/api/stn.aspx'
  payload = {'cmd': 'stns', 'key': KEY, 'json': 'y'}

  r = requests.get(urlEndpoint, payload)
  print(r.url)
  print(r.status_code)
  if (r.status_code == 200):
    with open(RESOURCES, 'w') as f:
      j = r.json()
      for station in j['root']['stations']['station']:
        
  else: 
    raise Exception('Request for {url} responded with error {err}'
        .format(url=urlEndpoint, err=r.status_code))


if __name__ == "__main__":
  updateStations()