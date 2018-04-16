import csv
import MySQLdb
import os

# read configuration from environment
mysql_db = os.environ['mysql_db']
directory = os.environ['directory_with_farsight_files']
sql_dump = os.environ['sql_dump']
table_name = 'farsight'

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
    f = open(sql_dump, 'w')
    #file.write(create_table_query)
    #file.close()
    print("Done: Table created")
    print("===================")

create_table()
