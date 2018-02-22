import os
import csv
from collections import OrderedDict

class Writer:
    'class to write new csvs'
    def __init__(self, records, file_path, file_name_root):
        self.records = records
        self.order_fieldnames()
        self.file_path = file_path
        self.file_name_root = file_name_root

    def write_updated_csv(self):
        pass

    def write_new_location_csv(self):
        with open(os.path.join(self.file_path, self.file_name_root + 'geocode_data.csv'), 'w') as f:
            writer = csv.writer(f, delimiter = ',')
            for record in self.records:
                if record.location:
                    fields = [record.id, record.location.lat, record.location.lng]
                    for k in self.specificities:
                        try:
                            fields.append(getattr(record.location, k))
                        except AttributeError:
                            fields.append('')
                    writer.writerow(fields)

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
        self.ordered_fieldnames = OrderedDict(zip(['id', 'lat', 'lng'], 3 * [None])).update(self.specificities)
