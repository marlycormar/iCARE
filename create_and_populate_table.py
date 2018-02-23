import csv
import MySQLdb
import os

# writing as many %s as the number of columns
number_columns = 55
#number_columns += 2 # accounting for columns file_name and study_id
format_strings = ','.join(['%s'] * number_columns)

# connecting to the database
mydb = MySQLdb.connect(host='localhost', user='root', db='iCARE')
cursor = mydb.cursor()

# setting the directory to the read the files from
directory = '/Users/marlycormar/Google Drive/CTS-IT/Tasks/20180220/data'

for file_name in os.listdir(directory):
    if file_name.endswith(".csv"):
        print(file_name)
        study_id = file_name.split('_')
        study_id = study_id[0] + '_' + study_id[1]

        # reading the data
        csv_data = csv.reader(file('../data/%s' %file_name), dialect=csv.excel_tab)
        csv_data.next() # skip the first line as it contains the column names

        # insert each row
        for row in csv_data:
            row = [study_id] + row      # consider improving this method of prepending
            row = [file_name] + row     # maybe modify the csv file first?
            #cursor.execute("INSERT INTO test VALUES(%s)" %format_strings, row)
    else:
        continue

# close the connection to the database.
mydb.commit()
cursor.close()

print("Done");

## todo: create method to undo changes if failure, and log failures
## with clear messages
