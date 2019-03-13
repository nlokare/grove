import argparse
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import pandas as pd
from uszipcode import SearchEngine

class FindStore(object):
  MAX_DISTANCE = 1000000.
  def __init__(self):
    self.store_locations = pd.read_csv('store-locations.csv')

  def format_response(self, dist, store_data, unit, output):  
    # type: (float, Dict[str, any], Optional[str]) -> Union[str, Dict[str, Union[str, float]]]
    rounded_dist = round(dist, 2)  # type: float
    if output == 'text':
      store_address = '%s. %s, %s %s' % (store_data['Address'], store_data['City'], store_data['State'], store_data['Zip Code']) 
      return 'The closest store is located at %s and is %s %s away' % (store_address, rounded_dist, unit)
    elif output == 'json':
      store_data_dict = store_data.to_dict()
      store_data_dict['distance'] = rounded_dist
      store_data_dict['distance_unit'] = unit
      return store_data_dict
    else:
      return 'Output must be "text" or "json", default is "text"'

  def calculate_distances(self, target_coords, unit):  
    # type: (Tuple[float, float], Optional[str]) -> Tuple[float, Dict[str, any]]
    closest_store_dist = self.MAX_DISTANCE  # type: int
    closest_store = {}  # type: Dict[str, any]
    for index, store in self.store_locations.iterrows():
      curr_store_coords = (store['Latitude'], store['Longitude'])  # type: Tuple[float, float]
      calc_distance = geodesic(target_coords, curr_store_coords)  # type: Dict[str, float]
      distance = calc_distance.km if unit == 'km' else calc_distance.mi
      if distance < closest_store_dist:
        closest_store_dist = distance
        closest_store = store
    return (closest_store_dist, closest_store)

  def find_by_address(self, address, unit, output):  # type: (str, Optional[str], Optional[str]) -> str
    geolocator = Nominatim(user_agent="Store Locator")
    loc = geolocator.geocode(address)  # type: Dict[str, any]
    target_address_coords = (loc.latitude, loc.longitude)  # type: Tuple[float, float]
    closest_store_dist, closest_store = self.calculate_distances(target_address_coords, unit)
    return self.format_response(closest_store_dist, closest_store, unit, output)

  def find_by_zip(self, zip, unit, output):  # type: (Union[str, int], Optional[str]) -> str
    search = SearchEngine(simple_zipcode=True)
    zipcode_loc = search.by_zipcode(zip).to_dict()  # type: Dict[str, any]
    target_address_coords = (zipcode_loc['lat'], zipcode_loc['lng'])  # type: Tuple[float, float]
    closest_store_dist, closest_store = self.calculate_distances(target_address_coords, unit)
    return self.format_response(closest_store_dist, closest_store, unit, output)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description='Find Store: \
      \n\tfind_store will locate the nearest store (as the vrow flies) from \
      \n\tstore-locations.csv, print the matching store address, as well as \
      \n\tthe distance to that store. \
      \n\nUsage: \
        \n\tfind_store --address="<address>" \
        \n\tfind_store --address="<address>" [--units=(mi|km)] [--output=text|json] \
        \n\tfind_store --zip=<zip> \
        \n\tfind_store --zip=<zip> [--units=(mi|km)] [--output=text|json]'
      )
  parser.add_argument("--address", help="Find nearest store to this address. If there are multiple best-matches, return the first.")
  parser.add_argument("--zip", help="Find nearest store to this zip code. If there are multiple best-matches, return the first.")
  parser.add_argument("--unit", help="Display units in miles or kilometers [default: mi]")
  parser.add_argument("--output", help="Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]")
  args = parser.parse_args()
  find_store = FindStore()
  if args.address:
    if args.unit and args.output:
      print find_store.find_by_address(args.address, args.unit, args.output)
    elif args.unit and args.output is None:
      print find_store.find_by_address(args.address, args.unit, 'text')
    elif args.unit is None and args.output:  
      print find_store.find_by_address(args.address, 'mi', args.output)
    else:
      print find_store.find_by_address(args.address, 'mi', 'text')
  elif args.zip:
    if args.unit and args.output:
      print find_store.find_by_zip(args.zip, args.unit, args.output)
    elif args.unit and args.output is None:
      print find_store.find_by_zip(args.zip, args.unit, 'text')
    elif args.unit is None and args.output:  
      print find_store.find_by_zip(args.zip, 'mi', args.output)
    else:
      print find_store.find_by_zip(args.zip, 'mi', 'text')
  else:
    print 'Please enter either an --address argument or --zip argument'
