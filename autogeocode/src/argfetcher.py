import configparser
import csv
import os
import googlemaps
from collections import OrderedDict


class ArgumentFetcher:
    def __init__(self):

        self.config_params = {
            'CSVFILE': ['csv_path', 'id_field', 'location_fields'],
            'APIKEYS': ['google_key', 'api_file'],
            'STATUS': ['started']
        }

        self.arg_list =  ['csv_path', 'id_field', 'location_fields', 'google_key', 'started', 'prev_fetched']


    @property
    def csv_path(self):
        return self.__csv_path

    @csv_path.setter
    def csv_path(self, path):
        try:
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                self.__csv_path = path
                print("Successfully read CSV file at {}".format(self.csv_path))
        except Exception as e:
            print(e)
            print('\nThere was an error opening the csv file. Please try again.')
            self.get_csv_path_from_user()

    def get_csv_path_from_user(self):
        self.csv_path = input("\n\nType the path to the csv file: ")

    @property
    def location_fields(self):
        return self.__location_fields

    @location_fields.setter
    def location_fields(self, fields):
        try:
            if isinstance(fields, str):
                fields = fields.split(',')
            with open(self.csv_path, 'r') as f:
                reader = csv.DictReader(f)
                bad_fields = [field for field in fields if field not in reader.fieldnames]
            if bad_fields:
                print("{} were not in the CSV file you provided. Please try again.".format(bad_fields))
                self.get_location_fields_from_user()
            else:
                self.__location_fields = fields
                print("Successfully read location fields {}.".format(fields))

        except Exception as e:
            print(e)
            print('\nThere was an error reading the location fields.  You provided {}.  Please try again'
                  .format(fields))
            self.get_location_fields_from_user()

    def get_location_fields_from_user(self):
        entry_method = input("\n\nEnter the names of the location fields in your spreadsheet, from most to least"
                             "specific. Press C to enter the location fields as a list separated by commas (e.g. "
                             "City/State/Country). Press 1 to enter them one at a time: ")

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

    @property
    def id_field(self):
        return self.__id_field

    @id_field.setter
    def id_field(self, id_field):
        try:
            with open(self.csv_path, 'r') as f:
                reader = csv.DictReader(f)
                if id_field not in reader.fieldnames:
                    print("{} was not in the CSV file you provided. Please try again.".format(id_field))
                else:
                    self.__id_field = id_field
                    print("Successfully read id fieldname {}.".format(id_field))

        except Exception as e:
            print(e)
            print('\nThere was an error reading the id_field.  You provided {}.  Please try again'
                  .format(id_field))
            self.get_id_field_from_user()

    def get_id_field_from_user(self):
        self.id_field = input("\n\nType the name of the record id column: ")

    @property
    def google_key(self):
        return self.__google_key

    @google_key.setter
    def google_key(self, key):
        try:
            gmaps = googlemaps.Client(key)
            self.__google_key = key
            print("Successfully read Google Maps API key.")
        except Exception as e:
            print(e)
            print('\nThere was an error using your Google Maps API key. Please try again.')
            self.get_google_key_from_user()

    def get_google_key_from_user(self, spreadsheet):
        spreadsheet.google_key = input("\n\nEnter your key for the Google Maps API: ")

    @property
    def started(self):
        return self.__started

    @started.setter
    def started(self, started):
        if started in ['Y', 'N']:
            if started =='Y':
                self.__started = 'started'
            else:
                self.__started = 'new'
        else:
            self.get_started_status_from_user()

    def get_started_status_from_user(self):
        started = input(
            "Are you reuploading a spreadsheet that has been partially completed by this program before? Y/N: ")
        if started == 'Y':
            self.started = 'Y'
        else:
            self.started = 'N'

    @property
    def prev_fetched(self):
        return self.__prev_fetched

    @prev_fetched.setter
    def prev_fetched(self, path):
        try:
            with open(path, 'r') as f:
                self.prev_fetched = csv.DictReader(f)
                self.__prev_fetched = path
                print("Successfully read previously fetched CSV file at {}".format(self.csv_path))
        except Exception as e:
            print(e)
            print('\nThere was an error opening the CSV file. Please try again.')
            self.get_prev_fetched_csv_from_user()

    def get_prev_fetched_csv_from_user(self):
        partial_file_path = os.path.splitext(self.csv_path)[0] + '_updated.csv'
        predicted_path_is_correct = input("Is the path to the partially completed spreadsheet (with suffix '_updated')\n"
                                       "{} \n Y/N ".format(partial_file_path))
        if predicted_path_is_correct == 'N':
            self.prev_fetched = input("Please enter the path to the to partially completed spreadsheet (with suffix '_updated')")
        else:
            self.prev_fetched = partial_file_path

    def read_config_file(self, file):
        config = configparser.ConfigParser()
        config.read(file)
        self.config = config
        config_dict = {}
        for section, atts in self.config_params.items():
            for att in atts:
                try:
                    config_dict[att] = self.config.get(section, att)
                except:
                    pass
        return config_dict

    def set_spreadsheet_args(self, dict):
        for key in dict:
            if dict[key]:
                setattr(self, key, dict[key])

    def check_for_missing_args(self):
        required_args_and_methods = OrderedDict([('csv_path', self.get_csv_path_from_user),
                                                ('id_field', self.get_id_field_from_user),
                                                ('location_fields', self.get_location_fields_from_user),
                                                ('google_key', self.get_google_key_from_user)])

        for arg, method in required_args_and_methods.items():
            if not hasattr(self, arg):
                method()

        if hasattr(self, 'started'):
            if self.started == 'Y':
                if not hasattr(self, 'prev_fetched'):
                    self.get_prev_fetched_csv_from_user()

    def gen_arguments_dict(self):
        arg_dict = {}
        for arg in self.arg_list:
            try:
                arg_dict[arg] = getattr(self, arg)
            except:
                pass
        return arg_dict

