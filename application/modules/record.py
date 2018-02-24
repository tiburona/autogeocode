from itertools import combinations
import geocoder
import googlemaps
from bingmaps.apiservices import LocationByQuery

class Record:
    'Class for a line in a csv file'

    def __init__(self, row_dict, spreadsheet):
        self.fields = row_dict
        self.spreadsheet = spreadsheet
        self.num_queries = 0
        self.location = None
        self.id = spreadsheet.id_field

    def fetch_geocoded_data(self):
        self.gen_location_arrays(self.spreadsheet.location_fields)
        for location_array in self.location_arrays:
            query_string = ",".join(location_array)
            if query_string in self.spreadsheet.cache:
                self.location = self.spreadsheet.cache[query_string]
            else:
                self.query_api(query_string)
            self.num_queries += 1
            if self.location or self.num_queries > 20:
                break

    def query_api(self, query_string):
        if(query_string is not None and query_string.strip()!=""):
            self.query_google(query_string)

    def gen_location_arrays(self, location_fields):
        locations = [self.fields[location_field] for location_field in location_fields]
        location_arrays = [locations]
        for s in [1, 2]:
            if len(locations) > s:
                location_arrays.extend([location_list for location_list in combinations(locations, len(locations) - s)])
        self.location_arrays = location_arrays

    def query_google(self, query):
        gmaps = googlemaps.Client(self.spreadsheet.api_keys['google'])
        result = gmaps.geocode(query)
        if len(result) > 0:
            self.location = Location(result, 'google')

class Location:
    def __init__(self, result, api):
        if api == 'google':
            self.google_init(result)
            self.src = 'google'

    def google_init(self, result):
        [setattr(self, key, result[0]['geometry']['location'][key]) for key in ['lat', 'lng']]
        components = result[0]['address_components']
        self.address_components = [(component['long_name'], component['types'][0]) for component in components]
        [self.__setattr__(component['types'][0], component['long_name']) for component in components]
        print(self.address_components)









