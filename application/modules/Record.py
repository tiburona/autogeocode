from itertools import combinations
import geocoder
import googlemaps
from bingmaps.apiservices import LocationByQuery

class Record:
    'Class for a line in a csv file'

    def __init__(self, row_dict, api_keys, location_fields):
        self.fields = row_dict
        self.api_keys = api_keys
        self.location_fields = location_fields
        self.num_queries = 0
        self.location = None

    def fetch_geocoded_data(self):
        self.gen_location_arrays(self.location_fields)
        for location_array in self.location_arrays:
            self.query_api(",".join(location_array))
            self.num_queries += 1
            if self.location or self.num_queries > 20:
                break

    def query_api(self, query_string):
        self.query_google(query_string)

    def gen_location_arrays(self, location_fields):
        locations = [self.fields[location_field] for location_field in location_fields]
        location_arrays = [locations]
        for s in [1, 2]:
            if len(locations) > s:
                location_arrays.extend([location_list for location_list in combinations(locations, len(locations) - s)])
        self.location_arrays = location_arrays

    def query_google(self, query):
        gmaps = googlemaps.Client(self.api_keys['google'])
        result = gmaps.geocode(query)
        if len(result) > 0:
            print(result)
            self.location = result[0]['geometry']['location']





