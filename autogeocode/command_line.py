import sys

from autogeocode.src import spreadsheet
from autogeocode.src import writer
from autogeocode.src import argreader


def main():
    if len(sys.argv) == 1:
        new_spreadsheet = spreadsheet.Spreadsheet()

    argument_reader = argreader.ArgumentReader(sys.argv[1], sys.argv[2])

    csv_file, location_fields, api_file, status, id_field, = argument_reader.spreadsheet_arguments()

    new_spreadsheet = spreadsheet.Spreadsheet(csv_file=csv_file, location_fields=location_fields, api_file=api_file,
                                              status=status, id_field=id_field)

    new_spreadsheet.fetch_geocoded_data()

    new_writer = writer.Writer(new_spreadsheet.records, new_spreadsheet.csv_file, new_spreadsheet.status)

    new_writer.write_files()


hello = 'hey'

print(hello)