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
    print("Starting: create_table")
    column_names = ["`study_id`", "`file_name`"]
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            # reading the data
            csv_data = csv.reader(file('../data/%s' %file_name))
            headers = csv_data.next()

            if(len(column_names) == 2):
                column_names = column_names + ['`' + field_name  + '`' for field_name in headers]

            else:
                for column in headers:
                    if not "`" + column + "`" in column_names:
                        column_names.append("`" + column + "`")

    # TODO: the field Existing_variation is biggg, it needs more than VARCHAR(350). 
    create_table_query = """CREATE TABLE IF NOT EXISTS """ + table_name + " (" + " VARCHAR(250),".join(column_names) + " VARCHAR(250))"
    cursor.execute(create_table_query)
    print("Done: Table created")
    print("===================")

def fill_table(table_name):
    print("Starting: fill_table")
    count = 0
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"): #and file_name.startswith("OtB"):
            #print(file_name)
            study_id = file_name.split('_')
            study_id = study_id[0] + '_' + study_id[1]

            # reading the data
            csv_data = csv.reader(file('../data/%s' %file_name))

            headers = csv_data.next()
            format_strings = ','.join(['%s'] * (len(headers) + 2)) # account for the fields study_id and file_name
            columns = ["`study_id`", "`file_name`"] + ['`' + field_name  + '`' for field_name in headers]
            columns = ",".join(columns)

            # insert each row
            for row in csv_data:
                # writing as many %s as the number of columns
                row = [file_name] + row     # maybe modify the csv file first?
                row = [study_id] + row      # consider improving this method of prepending
                cursor.execute("INSERT INTO %s (%s) VALUES (%s)" %(table_name, columns, format_strings), row)
                count += 1

    print("Done: Tabled filled. %s records created" %count)
    print("==============================================")


def add_indexes(table_name, indexes):
    print("Starting: add_indexes")

    for field_name in indexes:
        cursor.execute("CREATE INDEX %s ON %s (%s)" %(field_name, table_name, field_name))

    print("Done: Indexes added")
    print("===================")

def change_field_type (table_name, field_names_types_pairs):
    print("Starting: change_field_type")

    for pair in field_names_types_pairs:
        cursor.execute("ALTER TABLE %s MODIFY %s %s" %(table_name, pair[0], pair[1]))

    print("Done: Field types updated")
    print("=========================")

create_table(table_name)
field_names_types_pairs = [("`Existing_variation`", "VARCHAR(500)")]
change_field_type(table_name, field_names_types_pairs)
fill_table(table_name)
add_indexes(table_name, ["study_id", "ChromosomeNo", "GeneName", "pMut"])

# commit the the table changes to the db
mydb.commit()

# close the connection to the database.
cursor.close()

print("Done");


## todo: create method to undo changes if failure, and log failures
## skip files that fail
## with clear messages
