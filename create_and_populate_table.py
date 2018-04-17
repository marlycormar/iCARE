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
    global sql_queries
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
    f = open(sql_dump, 'w')
    f.write("CREATE DATABASE IF NOT EXISTS %s;\n" %mysql_db)
    f.write("USE %s;\n" %mysql_db)
    f.write("""CREATE TABLE IF NOT EXISTS """ + table_name + " (" + " VARCHAR(250),".join(column_names) + " VARCHAR(250)); \n")
    f.close();
    print("Done: Queries to insert tables created")
    print("===================")

def fill_tables_queries():
    print("Starting: fill_tables_queries")
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
                f = open(sql_dump, 'a')
                if count % 10000 == 0:
                    print "%s records inserted" %count
                f.write(str(("INSERT INTO %s (%s) VALUES (%s)" %(table_name, columns, format_strings), row)))
                f.close();
                count += 1
    print("Done: Queries added. %s records created" %count)
    print("==============================================")


def add_indexes(indexes):
    print("Starting: add_indexes")
    global sql_queries

    for field_name in indexes:
        sql_queries += "CREATE INDEX %s ON %s (%s)" %(field_name, table_name, field_name)

    print("Done: Indexes added")
    print("===================")

def change_field_type (field_names_types_pairs):
    print("Starting: change_field_type")
    global sql_queries

    for pair in field_names_types_pairs:
        sql_queries += "ALTER TABLE %s MODIFY %s %s" %(table_name, pair[0], pair[1])

    print("Done: Field types updated")
    print("=========================")


def queries_to_local_mysql_db():
    global sql_queries
    mysql_host = os.environ['mysql_host']
    mysql_user = os.environ['mysql_user']
    mysql_password = os.environ['mysql_password']
    mydb = MySQLdb.connect(host=mysql_host, user=mysql_user, db=mysql_db, passwd=mysql_password)
    cursor = mydb.cursor()
    cursor.execute(sql_queries)
    mydb.commit()
    cursor.close()




create_tables_queries()
#field_names_types_pairs = [("`Existing_variation`", "VARCHAR(500)")]
#change_field_type(field_names_types_pairs)
fill_tables_queries()
#add_indexes(["study_id", "ChromosomeNo", "GeneName", "pMut"])
#queries_to_local_mysql_db()
print("Done");


## todo: create method to undo changes if failure, and log failures
## skip files that fail
## with clear messages


## todo:
## add comments on create_local_mysql_table
## remove paraenthesis in the print stemetns
