import csv
import os
from .record import Record
from .location import Location
from collections import OrderedDict

class Spreadsheet:
    'Class for a single csv'

    def __init__(self, csv_path=None, location_fields=None, google_key=None, id_field=None, started=None, prev_fetched=None):
        self.cache = {}
        for var, method, string in [(csv_path, self.get_csv_path, 'csv_path'),
                                    (google_key, self.get_google_key, 'google_key'),
                                    (location_fields, self.get_location_fields, 'location_fields'),
                                    (id_field, self.get_id_field, 'id_field'),
                                    (started, self.get_started_status, 'started')]:
            if var:
                setattr(self, string, var)
            else:
                method()
        try:
            self.location_fields = self.location_fields.split(',')
        except:
            pass
        self.reader = csv.DictReader(open(self.csv_path, "r", newline="", encoding="utf-8"))
        self.failures = []
        self.api_keys = {'google': self.google_key}
        if self.started == 'started':
            self.create_cache_from_previously_fetched()

    def get_location_fields(self):
        print("The column headings in your CSV file are:")
        print(self.reader.fieldnames)
        entry_method = input('\n\nPress C to enter the location fields as a list separated by commas. '
                             'Press 1 to enter them one at a time: ')

        if entry_method == '1':
            more_location_fields = True
            location_fields = []
            while more_location_fields:
                next_location_field = input(
                    "Type the next location field, or type END_FIELDS if there are no more: ")
                more_location_fields = next_location_field != 'END_FIELDS' and len(location_fields) < 21
                if next_location_field != 'END_FIELDS':
                    location_fields.append(next_location_field)

            self.location_fields = location_fields

        else:
            self.location_fields = input('Enter a list of fields separated by commas: ').split(',')


    def get_api_file(self):
        print("\n\nA file with the API keys should be in the format <keytype>=<keyvalue>")
        self.api_file = input("Type the path to a file with the api keys: ")
        while True:
            try:
                self.gen_api_dict()
                print("Generated API key dictionary")
                break
            except Exception as e:
                print(e)
                print("There was an error reading the API file, please try again.")


    def gen_api_dict(self):
        with open(self.api_file, 'r') as f:
            self.api_keys = dict([line.replace("\n", '').split('=') for line in f.readlines() if len(line) > 1])

    def get_google_key(self):
        self.google_key = input("\n\nEnter your key for the Google Maps API: ")



    def get_csv_path(self):
        while True:
            self.csv_file = input("\n\nType the path to the csv file: ")
            try:
                f = open(self.csv_path, "r", newline="", encoding='utf-8')
                self.reader = csv.DictReader(f, dialect='excel')
                print("found and read CSV file")
                break
            except Exception as e:
                print(e)
                print("There was an error reading the CSV file, please try again")

    def get_id_field(self):
        self.id_field = input("\n\nType the name of the record id column: ")

    def get_started_status(self):
        started = input("Are you reuploading a spreadsheet that has been partially completed by this program before? Y/N: ")
        if started == 'Y':
            self.started = 'started'
        else:
            self.started = 'new'

    def create_cache_from_previously_fetched(self):
        self.get_path_to_partial_file()
        self.get_fieldnames_of_partial_file()
        self.populate_cache()

    def get_path_to_partial_file(self):
        self.partial_file_path = os.path.splitext(self.csv_file)[0] + '_updated.csv'
        predicted_path_correct = input("Is the path to the partially completed spreadsheet (with suffix '_updated')\n"
                               "{} \n Y/N ".format(self.partial_file_path))
        if predicted_path_correct == 'N':
            self.partial_file_path = ("Please enter the path to the to partially completed spreadsheet (with suffix '_updated')")

    def get_fieldnames_of_partial_file(self):
        with open(self.partial_file_path, "r", encoding='utf-16') as f:
            firstline = f.readline().replace('\n', '').split(',')
            self.location_result_fieldnames = firstline[firstline.index('lat'):]

    def populate_cache(self):
        with open(self.partial_file_path, "r", encoding='utf-16') as f:
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
        [record.fetch_geocoded_data() for record in self.records]
