import os

dir = os.path.dirname(__file__)
with open(os.path.join(dir, "..", "resources", "stationAbbrToStationName.json"), "r") as f:
  print(f.read())
  print("helloworld")
  print(os.getcwd())