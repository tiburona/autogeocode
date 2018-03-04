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

    def write_file(self, fieldnames, suffix):
        if self.already_started:
            filename = os.path.join(self.file_path, self.file_name_root + '.csv')
            f = open(filename, 'a')
            self.writer = csv.writer(f, delimiter=',')
        else:
            f = open(os.path.join(self.file_path, self.file_name_root + suffix + '.csv'), 'w')
            self.writer = csv.writer(f, delimiter=',')
            self.writer.writerow(fieldnames)
        self.write_records(suffix)
        f.close()

    def write_files(self, files_to_write = ['new_location_csv', 'updated_csv']):
        if 'new_location_csv' in files_to_write:
            fieldnames = [self.id_field] + self.ordered_location_fieldnames
            self.write_file(fieldnames, '_locations')
        if 'updated_csv' in files_to_write:
            fieldnames =  self.pre_existing_fields + self.ordered_location_fieldnames
            self.write_file(fieldnames, '_updated')

    def write_records(self, suffix):
        for record in self.records:
            if suffix == '_updated':
                fields = [v for v in record.fields.values()]
            else:
                fields = [record.fields[self.id_field]]
            if record.location:
                for k in self.ordered_location_fieldnames:
                    try:
                        fields.append(getattr(record.location, k))
                    except AttributeError:
                        fields.append('')
            if suffix == '_updated' or record.location:
                self.writer.writerow(fields)

    def get_unique_address_components(self):
        self.unique_address_components = set([fieldname for rec in self.records for fieldname in rec.location.__dict__]) - \
                                         {'lat', 'lng', 'src', 'address_components', 'query'}

    def get_specificities(self):
        specificities = {}
        for fieldname in self.unique_address_components:
            specificities[fieldname] = self.calc_specificity(fieldname)
        self.specificities = OrderedDict(sorted(specificities.items(), key=lambda t: t[1]))

    def calc_specificity(self, fieldname):
        specificity_sum = 0; count = 0
        for record in self.records:
            address_components = [address_component[1] for address_component in record.location.address_components]
            if fieldname in address_components:
                count += 1
                specificity_sum += (address_components.index(fieldname) + 1) / len(address_components)
                break
        return specificity_sum / count

    def order_location_fieldnames(self):
        self.get_unique_address_components()
        self.get_specificities()
        self.ordered_location_fieldnames = ['lat', 'lng'] + [key for key in self.specificities.keys()]
