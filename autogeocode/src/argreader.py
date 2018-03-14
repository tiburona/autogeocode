import configparser

class ArgumentReader:
    def __init__(self):

        self.csv_path = None
        self.location_fields = None
        self.google_key = None
        self.started = None
        self.id_field = None
        self.prev_fetched = None

        self.config_params = {
            'CSVFILE':  ['path', 'id_field', 'location_fields'],
            'APIKEYS': ['google_key', 'api_file'],
            'STATUS': ['started']
        }

    def read_config_file(self, file):
        config = configparser.ConfigParser()
        config.read(file)
        self.config = config
        [self.get_argument(att, section) for section, atts in self.config_params.items() for att in atts]

    def get_argument(self, att, section):
        try:
            arg = self.config.get(section, att)
            setattr(self, att, arg)
        except:
            print('Could not get ' + att + ' from config file')

    def spreadsheet_arguments(self):
        # return (self.csv_file, self.location_fields, self.google_key, self.started, self.id_field)
        return {
            'csv_path': self.path, 'location_fields': self.location_fields, 'google_key': self.google_key,
            'started': self.started, 'id_field': self.id_field, 'prev_fetched': self.prev_fetched
        }
