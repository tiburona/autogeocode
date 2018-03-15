from itertools import combinations
import geocoder
import googlemaps
from bingmaps.apiservices import LocationByQuery
from .location import Location

class Record:
    'Class for a line in a csv file'

    def __init__(self, row_dict, spreadsheet):
        self.fields = row_dict
        self.spreadsheet = {'cache': spreadsheet.cache, 'api_keys': spreadsheet.api_keys,
                            'id_field': spreadsheet.id_field, 'location_fields': spreadsheet.location_fields,
                            'failures': spreadsheet.failures}
        self.num_queries = 0
        self.location = None

    def fetch_geocoded_data(self):
        self.gen_location_arrays()
        for location_array in self.location_arrays:
           self.generate_and_send_query(location_array)
           self.num_queries += 1
           if self.location or self.num_queries > 20:
               break
        if self.num_queries > 20:
            self.spreadsheet['failures'].append(self.fields[self.spreadsheet['id_field']])

    def gen_first_location_array(self):
        location_fields = [self.fields[location_field] for location_field in self.spreadsheet['location_fields']]
        return [location_field for location_field in location_fields if location_field is not '']

    def gen_location_arrays(self):
        locations = self.gen_first_location_array()
        location_arrays = [locations]
        for s in [1, 2]:
            if len(locations) > s:
                location_arrays.extend([location_list for location_list in combinations(locations, len(locations) - s)])
        self.location_arrays = location_arrays

    def generate_and_send_query(self, location_array):
        query_string = ",".join([field for field in location_array if len(field)])
        if self.has_non_whitespace_chars(query_string):
            if query_string in self.spreadsheet['cache']:
                self.location = self.spreadsheet['cache'][query_string]
            else:
                self.query_api(query_string)

    def has_non_whitespace_chars(self, query_string):
        return len(query_string.strip().replace(',', ''))

    def query_api(self, query_string):
        self.query_google(query_string)

    def query_google(self, query):
        gmaps = googlemaps.Client(self.spreadsheet['api_keys']['google'])
        result = gmaps.geocode(query)
        if len(result) > 0:
            self.location = Location(result, 'google', query)
            self.spreadsheet['cache'][query] = self.location

    def get_location_field(self, field):
        try:
            return getattr(self.location, field)
        except AttributeError:
            return ''









