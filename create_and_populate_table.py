import csv
import MySQLdb

# connecting to the database
mydb = MySQLdb.connect(host='localhost', user='root', db='iCARE')
cursor = mydb.cursor()

# creating the new columns
file_name = 'UFH_00077_001_S5_R1_001_FarsightAllVars_VI0209_587genelist.csv';
study_id = file_name.split('_')
study_id = study_id[0] + '_' + study_id[1]

# reading the data
csv_data = csv.reader(file('../data/%s' %file_name))
csv_data.next() # skip the first line

# writing as many %s as the number of columns
number_columns = 55
number_columns += 2 # accounting for columns file_name and study_id
format_strings = ','.join(['%s'] * number_columns)

# insert each row
for row in csv_data:
    row = [study_id] + row      # consider improving this method of prepending
    row = [file_name] + row     # maybe modify the csv file first?
    cursor.execute("INSERT INTO test VALUES(%s)" %format_strings, row)

# close the connection to the database.
mydb.commit()
cursor.close()

print("Done");

## todo: create method to undo changes if failure, and log failures
## with clear messages
