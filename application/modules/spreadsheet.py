import csv
from modules.record import Record

class Spreadsheet:
    'Class for a single csv'

    def __init__(self, csv_file=None, location_fields=None, api_file=None, id_field=None, status=None):
        for var, method, string in [(csv_file, self.get_csv_file, 'csv_file'),
                                    (api_file, self.get_api_file, 'api_file'),
                                    (location_fields, self.get_location_fields, 'location_fields'),
                                    (id_field, self.get_id_field, 'id_field'),
                                    (status, self.get_status, 'status')]:
            if var:
                setattr(self, string, var)
            else:
                method()
        try:
            self.location_fields = self.location_fields.split(',')
        except:
            pass
        self.reader = csv.DictReader(open(self.csv_file, "r", newline="", encoding="utf-8"))
        self.gen_api_dict()
        self.cache = {}

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
            self.location_fields = input('Enter a list of fields separated by commas').split(',')


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

    def get_csv_file(self):
        while True:
            self.csv_file = input("\n\nType the path to the csv file: ")
            try:
                f = open(self.csv_file, "r", newline="", encoding="utf-8")
                self.reader = csv.DictReader(f)
                print("found and read CSV file")
                break
            except Exception as e:
                print(e)
                print("There was an error reading the CSV file, please try again")


    def get_id_field(self):
        self.id_field = input("\n\nType the name of the record id column: ")

    def get_status(self):
        status = input("Are you reuploading a spreadsheet that has been partially completed by this program before? Y/N")
        if status == 'Y':
            self.status = 'already_started'
        else:
            self.status = 'new'

    def split_field_string(self):
        if(hasattr(self.location_fields, 'split')):
            self.location_fields = self.location_fields.split(",")

    def fetch_geocoded_data(self):
        if self.status == 'started':
            self.records = [Record(row, self) for row in self.reader if len(row['lat']) > 1]
        else:
            self.records = [Record(row, self) for row in self.reader]
        [record.fetch_geocoded_data() for record in self.records]







