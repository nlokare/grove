## Code Summary ##

`find_store.py` uses the geopy and uszipcode libraries to convert address or zip codes to lat/long coordinates for distance comparisons

1. `pip install -r requirements.txt`
2. `python find_store.py -h'` for a list of accepted arguments
3. `pyhton find_store.py [ARGS]` to find the nearest store based on address or zip

## Assumptions ##

I assumed that there would be one uniquely distinct closest store based on the precision of the distance calculations and return the result accordingly.

## Testing ##

Run `python test.py` to run the unit tests
