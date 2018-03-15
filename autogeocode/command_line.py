import argparse
from collections import OrderedDict

from autogeocode.src import spreadsheet
from autogeocode.src import writer
from autogeocode.src import argfetcher

args_to_help = {
    '--config': 'path to the config file',
    '--config_example': 'print an example config file',
    '--csv_path':'the path to the input csv file',
    '--location_fields': 'a comma-separated list of field names with location information in the csv file. E.g. '
                         'City,State,Country. Location field names should go from more to less specific.',
    '--google_key': 'key for the Google Maps Api',
    '--id_field': 'column name for the unique record identifier in the input spreadsheet',
    '--started': 'A Y value indicates that this some records for this spreadsheet have been fetched already.  Any other '
                 'value results in the default behavior, assuming a new spreadsheet.',
    '--prev_fetched': "If some records for the spreadsheet have been fetched before, this is the path to the updated "
                      "spreadsheet with the fetched data (the one with 'updated' in the file name)."
}


def main():

    argname_to_argvar = OrderedDict.fromkeys(['csv_path','location_fields', 'id_field', 'google_key','started',
                                              'prev_fetched'])

    parser = argparse.ArgumentParser()
    [parser.add_argument(arg, help=help) for arg, help in args_to_help.items()]
    args = parser.parse_args()

    argument_fetcher = argfetcher.ArgumentFetcher()

    if args.config:
        argname_to_argvar.update(argument_fetcher.read_config_file(args.config))


    for arg_name in argname_to_argvar:
        try:
            if getattr(args, arg_name) is not None:
                argname_to_argvar[arg_name] = getattr(args, arg_name)
        except:
            print("I don't know the argument {}.  I'm going to ignore it.".format(arg_name))

    argument_fetcher.set_spreadsheet_args(argname_to_argvar)

    argument_fetcher.check_for_missing_args()

    new_spreadsheet = spreadsheet.Spreadsheet(**argument_fetcher.gen_arguments_dict())

    new_spreadsheet.fetch_geocoded_data()

    new_writer = writer.Writer(new_spreadsheet.records, new_spreadsheet.csv_path)

    new_writer.write_files()


def usage():
    print('Autogeocode takes tabular data in csv format that has location information in some columns, looks up the '
          'location using the Google Maps API, and writes three csv files into the same directory: one updated '
          'spreadsheet with columns at the end for latitude, longitude, and the other location fields fetched from the '
          'API, and one list of records for which lookup did not return a result.\n\n')
    print('The program assumes that records are stored in rows, that columns are named, and that the spreadsheet has a '
          'column with a unique identifier for each record.\n\n')
    print('The user can specify inputs with a formatted configuration file, with command line arguments when the '
          'program is run, or by responding to prompts at the command line.')
    lines_to_print = [
        'autogeocode '
    ]


if __name__ == '__main__':
    main()

