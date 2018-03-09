from modules.spreadsheet import Spreadsheet
import sys

#Create a set of args read in from input parameters. If any aren't passed, the CLI will challenge the user to provide the information
args = {}

#The first param can be a csv file with location data
if len(sys.argv) > 1 :
      print ("\n"+sys.argv[1])
      args.update({'csv_file':sys.argv[1]})

#The second param can be a text file with api keys
if len(sys.argv) > 2 :
      print ("\n"+sys.argv[2])
      args.update({'api_file':sys.argv[2]})

#The third param can be a comma separated list of location fields
if len(sys.argv) > 3 :
      print ("\n"+sys.argv[3])
      args.update({'location_fields':sys.argv[3]})

spreadsheet = Spreadsheet(**args)


spreadsheet.fetch_geocoded_data()

print(spreadsheet.location_fields)