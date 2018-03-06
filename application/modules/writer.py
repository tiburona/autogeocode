import os
import csv
from collections import OrderedDict

class Writer:
    'class to write new csvs'

    def __init__(self, records, csv_file, status):
        self.records = records
        self.csv_file = csv_file
        self.get_path_and_basename()
        self.set_fieldnames()
        self.already_started = (status == 'started')

    def get_path_and_basename(self):
        self.file_path, basename = os.path.split(self.csv_file)
        self.file_name_root, ext = os.path.splitext(basename)

    def set_fieldnames(self):
        self.order_location_fieldnames()
        self.pre_existing_fields = [key for key in self.records[0].fields.keys()]
        self.id_field = self.records[0].spreadsheet['id_field']

    def write_files(self, suffixes_of_files_to_write=['_locations', '_updated', '_failures']):
        suffix_to_fieldnames = {
            '_locations': [self.id_field] + self.ordered_location_fieldnames,
            '_updated': self.pre_existing_fields + self.ordered_location_fieldnames,
            '_failures': [self.id_field]
        }
        [self.write_file(suffix, suffix_to_fieldnames[suffix]) for suffix in suffixes_of_files_to_write]

    def write_file(self, suffix, fieldnames,):
        filename = os.path.join(self.file_path, self.file_name_root + suffix + '.csv')
        self.generate_writer(filename, 'w')
        self.writer.writerow(fieldnames)
        self.write_records(suffix)
        self.f.close()

    def generate_writer(self, filename, mode):
        self.f = open(filename, mode)
        self.writer = csv.writer(self.f, delimiter=',')

    def write_records(self, suffix):
        for record in self.records:
            fields = self.generate_fields_list(record, suffix)
            if suffix == '_failures':
                if not record.location: self.writer.writerow(fields)
            else:
                if suffix == '_updated' or record.location: self.writer.writerow(fields)

    def generate_fields_list(self, record, suffix):
        if suffix == '_updated':
            fields = [v for v in record.fields.values()]
        else:
            fields = [record.fields[self.id_field]]

        if record.location and suffix != '_failures':
            for fieldname in self.ordered_location_fieldnames:
                fields.append(record.get_location_field(fieldname))
        return fields

    def order_location_fieldnames(self):
        self.get_unique_address_fieldnames()
        self.get_field_specificities()
        self.ordered_location_fieldnames = ['lat', 'lng'] + [key for key in self.specificities.keys()]

    def get_unique_address_fieldnames(self):
        self.unique_address_fieldnames = set([key for rec in self.records if rec.location for key in rec.location.address_components])

    def get_field_specificities(self):
        specificities = {}
        for fieldname in self.unique_address_fieldnames:
            specificities[fieldname] = self.calculate_field_specificity(fieldname)
        self.specificities = OrderedDict(sorted(specificities.items(), key=lambda t: t[1]))

    def calculate_field_specificity(self, fieldname):
        specificity_sum = 0
        count = 0
        for record in self.records:
            address_components = [address_component for address_component in record.location.address_components]
            if fieldname in address_components:
                count += 1
                specificity_sum += (address_components.index(fieldname) + 1) / len(address_components)
                break
        return specificity_sum / count






