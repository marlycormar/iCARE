import csv
import MySQLdb
import os

# read configuration from environment
mysql_db = os.environ['mysql_db']
directory = os.environ['directory_with_farsight_files']
sql_dump = os.environ['sql_dump']
table_name = 'farsight'

def create_tables_queries():
    print("Starting: create_tables_queries")
    column_names = ["`study_id`", "`file_name`"]
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            # reading the data
            csv_data = csv.reader(file('%s/%s' % (directory, file_name)))
            headers = csv_data.next()

            if(len(column_names) == 2):
                column_names = column_names + ['`' + field_name  + '`' for field_name in headers]
                column_names = [column.lower() for column in column_names]

            else:
                for column in headers:
                    if not "`" + column.lower() + "`" in column_names:
                        column_names.append("`" + column.lower() + "`")

    # TODO: the field Existing_variation is biggg, it needs more than VARCHAR(350).
    f = open(sql_dump, 'w')
    f.write("CREATE DATABASE IF NOT EXISTS %s;\n" %mysql_db)
    f.write("USE %s;\n" %mysql_db)
    f.write("CREATE TABLE IF NOT EXISTS " + table_name + " (" + " VARCHAR(250),".join(column_names) + " VARCHAR(250));\n")
    f.close();
    print("Done: Queries to insert tables created")
    print("===================")


def fill_tables_queries():
    print("Starting: fill_tables_queries")
    count = 0
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv") and file_name.startswith("UFH"):
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
                f = open(sql_dump, 'a')
                if count % 10000 == 0:
                    print "%s records inserted" %count
                f.write(str("INSERT INTO %s (%s) VALUES %s;\n" %(table_name, columns, tuple(row))))
                f.close()
                count += 1
    print("Done: Queries added. %s records created" %count)
    print("==============================================")


def add_indexes(indexes):
    print("Starting: add_indexes")
    f = open(sql_dump, 'a')
    f_read = open(sql_dump, 'r').read()

    for field_name in indexes:
        if f_read.find(field_name):
            f.write("CREATE INDEX %s ON %s (%s);\n" %(field_name, table_name, field_name))

    f.close()

    print("Done: Indexes added")
    print("===================")


def change_field_type (field_names_types_pairs):
    print("Starting: change_field_type")
    f = open(sql_dump, 'a')
    f_read = open(sql_dump, 'r').read()

    for pair in field_names_types_pairs:
        if f_read.find(pair[0]):
            f.write("ALTER TABLE %s MODIFY %s %s;\n" %(table_name, pair[0], pair[1]))

    f.close()

    print("Done: Field types updated")
    print("=========================")


def queries_to_local_mysql_db():
    print "Starting: queries_to_local_mysql_db"
    mysql_host = os.environ['mysql_host']
    mysql_user = os.environ['mysql_user']
    mysql_password = os.environ['mysql_password']
    mydb = MySQLdb.connect(host=mysql_host, user=mysql_user, passwd=mysql_password)
    cursor = mydb.cursor()

    for line in open(sql_dump):
        cursor.execute(line)

    mydb.commit()
    cursor.close()
    print "Done: Data saved to local mysql db."
    print("===================")



create_tables_queries()
field_names_types_pairs = [("`existing_variation`", "VARCHAR(500)")]
change_field_type(field_names_types_pairs)
fill_tables_queries()
add_indexes(["`study_id`", "`chromosomeno`", "`genename`", "`pmut`"])
#queries_to_local_mysql_db()
print("Done");


## todo: create method to undo changes if failure, and log failures
## skip files that fail
## with clear messages

