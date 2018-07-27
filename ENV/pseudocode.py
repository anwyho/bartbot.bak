import requests
import urllib as url

KEY = 'ZSBD-57UA-9TVT-DWE9'


r = requests.get('http://api.bart.gov/api/etd.aspx?cmd=etd&orig=rock&key={key}&dir=n&json=y'.format(key=KEY))
if (r.status_code == 200):
  j = r.json()
  print(j['root']['date'])