import csv
import MySQLdb
import os

# read configuration from environment
#mysql_host = os.environ['mysql_host']
#mysql_user = os.environ['mysql_user']
#mysql_password = os.environ['mysql_password']
mysql_db = os.environ['mysql_db']
directory = os.environ['directory_with_farsight_files']
table_name = 'farsight'

# connecting to the database

sql_queries = ''

def create_table():
    print("Starting: create_table")
    column_names = ["`study_id`", "`file_name`"]
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            # reading the data
            csv_data = csv.reader(file('%s/%s' % (directory, file_name)))
            headers = csv_data.next()

            if(len(column_names) == 2):
                column_names = column_names + ['`' + field_name  + '`' for field_name in headers]

            else:
                for column in headers:
                    if not "`" + column + "`" in column_names:
                        column_names.append("`" + column + "`")

    # TODO: the field Existing_variation is biggg, it needs more than VARCHAR(350).
    create_table_query = """CREATE TABLE IF NOT EXISTS """ + table_name + " (" + " VARCHAR(250),".join(column_names) + " VARCHAR(250))"
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
            csv_data = csv.reader(file('%s/%s' % (directory, file_name)))

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


def create_mysql_table():
    mydb = MySQLdb.connect(host=mysql_host, user=mysql_user, db=mysql_db, passwd=mysql_password)
    cursor = mydb.cursor()

    cursor.execute(sql_queries)

    # commit the the table changes to the db
    mydb.commit()

    # close the connection to the database.
    cursor.close()



create_table(table_name)
field_names_types_pairs = [("`Existing_variation`", "VARCHAR(500)")]
change_field_type(table_name, field_names_types_pairs)
fill_table(table_name)
add_indexes(table_name, ["study_id", "ChromosomeNo", "GeneName", "pMut"])



print("Done");


## todo: create method to undo changes if failure, and log failures
## skip files that fail
## with clear messages
