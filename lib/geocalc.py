'''
This module can be imported or run from terminal

Examples (terminal):
  $ python geo_distance.py -lat1 37.2967792 -lng1 -121.9574965 -lat2 37.4314848 -lng2 -121.9199879
  15.341004008222285

  $ python geo_distance.py -lat1 37.2967792 -lng1 -121.9574965 -lat2 37.4314848 -lng2 -121.9199879 -u km
  5.608415470539164

  $ python geo_distance.py -lat1 37.2967792 -lng1 -121.9574965 -lat2 37.4314848 -lng2 -121.9199879 -u mi
  9.525821983444885
'''
from math import radians, cos, sin, asin, sqrt
from typing import Tuple


def distance(point1: Tuple, point2: Tuple, measurement: str ='') -> float:
  '''
  Get two geological locations as latitute and longtitute, and distance unit selection as km or mi and 
  returns distance in specified unit

  paramters:
    Inputs
      (lat1: float, lng1: float), (lat2: float, lng2: float), 'km/mi' : str 
    Output
      float
  '''
  earth_radius = {'km': 6371, 'mi': 3956}
  radius = earth_radius.get(measurement.lower(), 6371)

  lat1 = radians(point1[0])
  lat2 = radians(point2[0])
  lng1 = radians(point1[1])
  lng2 = radians(point2[1])

  dlng = lng2 - lng1
  dlat = lat2 - lat1
  a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
  c = 2 * asin(sqrt(a))

  return c * radius


def get_args():
  # Only used when this module is executed from terminal, so I prefer to keep these imports here rahter than top
  import sys
  import argparse

  parser = argparse.ArgumentParser(description="Get altitute and longtitite to calculate distance")
  parser.add_argument("-lat1", "--latitute1", type=float, help="First latitute")
  parser.add_argument("-lng1", "--langtitute1", type=float, help="First longtitute")
  parser.add_argument("-lat2", "--latitute2", type=float, help="Second latitute")
  parser.add_argument("-lng2", "--langtitute2", type=float, help="Second longtitute") 
  parser.add_argument('-u', "--measurement", choices=['mi', 'km'], default='km', help="Measurement Unit (Kilometers/miles)") 
  if len(sys.argv) == 1:
      parser.print_help(sys.stderr)
      print("\n")
      sys.exit(1)
  args = parser.parse_args()
  return (args.latitute1,args.langtitute1), (args.latitute2,args.langtitute2), args.measurement



if __name__ == "__main__":
  point1, point2, measurement = get_args()
  d = distance(point1, point2, measurement)
  print(d)
