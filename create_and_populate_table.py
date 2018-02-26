import csv
import MySQLdb
import os

# connecting to the database
mydb = MySQLdb.connect(host='localhost', user='root', db='iCARE')
cursor = mydb.cursor()

# setting the directory to the read the files from
directory = '/Users/marlycormar/Google Drive/CTS-IT/Tasks/20180220/data'

table_name = 'farsight'

def create_table(table_name):
    column_names = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            # reading the data
            csv_data = csv.reader(file('../data/%s' %file_name))
            headers = csv_data.next()

            if(len(column_names) == 0):
                column_names = ['`' + field_name  + '`' for field_name in headers]

            else:
                for column in headers:
                    if not "`" + column + "`" in column_names:
                        column_names.append("`" + column + "`")

    # TODO: the field Existing_variation is biggg, it needs more than VARCHAR(350). Using text for now but
    # need to improve this.
    create_table_query = """CREATE TABLE IF NOT EXISTS """ + table_name + " (" + " TEXT,".join(column_names) + " TEXT)"
    cursor.execute(create_table_query)

def fill_table(table_name):
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"): #and file_name.startswith("OtB"):
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
                cursor.execute("INSERT INTO %s (%s) VALUES (%s)" %(table_name, columns, format_strings), row)


create_table(table_name)
fill_table(table_name)

# commit the the table changes to the db
mydb.commit()

# close the connection to the database.
cursor.close()

print("Done");




## todo: create method to undo changes if failure, and log failures
## skip files that fail
## with clear messages
