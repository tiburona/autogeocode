import csv
from .record import Record
from .location import Location
from collections import OrderedDict

class Spreadsheet:
    """Class to represent the input CSV file, build a cache of previously fetched records, and start record fetching"""

    def __init__(self, csv_path=None, location_fields=None, google_key=None, id_field=None, started=None,
                 **kwargs):
        """
        Keyword args:
            csv_path (str, optional): Path to the input CSV file.  If none is provided, the user will be prompted.
            location_fields(str or list, optional): A comma-separated string with fieldnames, or a list of fieldnames,
            for fields that contain information.
            google_key(str, optional): A key to the Google Maps API.
            id_field(str, optional): The name of the field that contains the unique record identifier.
            started(str, optional): A value to indicate whether geocoded data for some of the records on the spreadsheet
            have been fetched previously. 'Y' will indicate that they have, and that prev_fetched must also be supplied
            as a keyword argument
        """

        self.csv_path = csv_path
        self.gen_reader()
        self.location_fields = location_fields
        self.google_key = google_key
        self.id_field = id_field
        self.started = started

        [setattr(self, arg_name, arg) for arg_name, arg in kwargs.items()]

        self.api_keys = {'google': self.google_key}
        self.cache = {}
        self.failures = []

        if self.started == 'started':
            self.create_cache_from_previously_fetched()

    def gen_reader(self):
        """"""
        self.reader = csv.DictReader(open(self.csv_path, "r"))

    def create_cache_from_previously_fetched(self):
        """
        """
        self.get_fieldnames_of_partial_file()
        self.populate_cache()

    def get_fieldnames_of_partial_file(self):
        with open(self.prev_fetched, "r", encoding='utf-16') as f:
            firstline = f.readline().replace('\n', '').split(',')
            self.location_result_fieldnames = firstline[firstline.index('lat'):]

    def populate_cache(self):
        with open(self.prev_fetched, "r", encoding='utf-16') as f:
            for row in csv.DictReader(f):
                result, query_string = self.read_prev_result(row)
                self.write_prev_result(query_string, result)

    def read_prev_result(self, row):
        location_fields = OrderedDict([(fieldname, row[fieldname]) for fieldname in self.location_fields
                                       if fieldname in row and len(row[fieldname])])
        result = OrderedDict([(key, val) for key, val in row.items() if key in self.location_result_fieldnames])
        query_string = ','.join([val for key, val in location_fields.items()])
        return [result, query_string]

    def write_prev_result(self, query_string, result):
        if any([val for _, val in result.items()]):
            self.cache[query_string] = Location(result, 'previously_fetched', query_string)
        else:
            self.cache[query_string] = None

    def fetch_geocoded_data(self):
        self.records = [Record(row, self) for row in self.reader]
        print("There are {} records to fetch.".format(len(self.records)))
        for i, record in enumerate(self.records):
            record.fetch_geocoded_data()
            if (i+1)%100 == 0:
                print("Fetched {} of {} records".format(i, len(self.records)))

