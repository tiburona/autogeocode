import configparser

class ArgumentReader:
    def __init__(self, flag, arg):
        self.flag = flag
        self.arg = arg
        self.analyze_args()

    def analyze_args(self):
        if self.flag == '-f':
            self.read_config_file()

    def read_config_file(self):
        config = configparser.ConfigParser()
        config.read(self.arg)
        self.csv_file = config.get('CSVFILE', 'path')
        self.location_fields = config.get('CSVFILE', 'location_fields')
        self.api_file = config.get('APIKEYS', 'api_file')
        self.status = config.get('STATUS', 'already_started')
        self.id_field = config.get('CSVFILE', 'id_field')

    def spreadsheet_arguments(self):
        return [self.csv_file, self.location_fields, self.api_file, self.status, self.id_field]



