
from autogeocode.src import spreadsheet, writer


print('/Users/katie/map-collections-autogeocode/csvs/small_test.csv')
print('/Users/katie/map-collections-autogeocode/keys.txt')
print('Island,City/Town/Hamlet,Stream,River/Creek,Lake/Pond/Reservoir,Island Group,Bay/Harbor,'
      'Department / Province / State,Country,Sea/Gulf/Strait,Ocean')


new_spreadsheet = spreadsheet.Spreadsheet(csv_file='/Users/katie/autogeocode/csvs/small_test.csv',
                                      api_file='/Users/katie/autogeocode/keys.txt',
                                      location_fields='Island,City/Town/Hamlet,Stream,River/Creek,Lake/Pond/Reservoir,'
                                                      'Island Group,Bay/Harbor,Department / Province / State,Country,Sea/Gulf/Strait,Ocean',
                                      id_field='Tracking Number',
                                      status='already_started')


#new_spreadsheet = spreadsheet.Spreadsheet()

new_spreadsheet.fetch_geocoded_data()

print(new_spreadsheet.location_fields)

new_writer = writer.Writer(new_spreadsheet.records, new_spreadsheet.csv_file, new_spreadsheet.status)

new_writer.write_files()

