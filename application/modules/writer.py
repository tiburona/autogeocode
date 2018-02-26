import os
import csv
from collections import OrderedDict

class Writer:
    'class to write new csvs'

    def __init__(self, records, csv_file, status):
        self.records = records
        self.csv_file = csv_file
        self.order_fieldnames()
        self.get_path_and_basename()
        self.already_started = (status == 'started')

    def get_path_and_basename(self):
        self.file_path, basename = os.path.split(self.csv_file)
        self.file_name_root, ext = os.path.splitext(basename)

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
            self.write_file(self.ordered_fieldnames,'_locations')
        if 'updated_csv' in files_to_write:
            location_fieldnames = self.ordered_fieldnames
            location_fieldnames.remove('id')
            fieldnames = [key for key in self.records[0].fields.keys()] + location_fieldnames
            self.write_file(fieldnames, '_updated')

    def write_records(self, suffix):
        for record in self.records:
            if suffix == '_updated':
                fields = [v for v in record.fields.values()]
            else:
                fields = [record.fields[record.spreadsheet['id']]]
            if record.location:
                fields.extend([record.location.lat, record.location.lng])
                for k in self.specificities:
                    try:
                        fields.append(getattr(record.location, k))
                    except AttributeError:
                        fields.append('')
            if suffix == '_updated' or record.location:
                self.writer.writerow(fields)

    def get_unique_address_components(self):
        self.unique_address_components = set([fieldname for rec in self.records for fieldname in rec.location.__dict__]) - \
                                         {'lat', 'lng', 'src', 'address_components'}
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

    def order_fieldnames(self):
        self.get_unique_address_components()
        self.get_specificities()
        self.ordered_fieldnames = ['id', 'lat', 'lng'] + [key for key in self.specificities.keys()]
