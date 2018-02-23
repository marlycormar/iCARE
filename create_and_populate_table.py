import csv
import MySQLdb
import os

def fill_table():
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv") and file_name.startswith("UFH"):
            print(file_name)
            study_id = file_name.split('_')
            study_id = study_id[0] + '_' + study_id[1]

            # reading the data
            csv_data = csv.reader(file('../data/%s' %file_name))

            headers = csv_data.next()
            format_strings = ','.join(['%s'] * len(headers))
            columns = ['`' + field_name  + '`' for field_name in headers]
            columns = ",".join(columns)

            # insert each row
            for row in csv_data:
                # writing as many %s as the number of columns
                #number_columns += 2 # accounting for columns file_name and study_id
                #row = [study_id] + row      # consider improving this method of prepending
                #row = [file_name] + row     # maybe modify the csv file first?
                cursor.execute("INSERT INTO test (%s) VALUES (%s)" %(columns, format_strings), row)
        else:
            continue


# connecting to the database
mydb = MySQLdb.connect(host='localhost', user='root', db='iCARE')
cursor = mydb.cursor()

# setting the directory to the read the files from
directory = '/Users/marlycormar/Google Drive/CTS-IT/Tasks/20180220/data'

fill_table()

# close the connection to the database.
mydb.commit()
cursor.close()

print("Done");




## todo: create method to undo changes if failure, and log failures
## skip files that fail
## with clear messages
