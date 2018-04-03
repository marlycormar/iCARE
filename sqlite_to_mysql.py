#! /usr/bin/env python
import os, re, fileinput, tempfile


def dump_sqlite_data(path_to_sqlitedb, path_to_mysql_dump):

    print("Starting: dump_sqlite_data")
    
    os.system("sqlite3 %s .dump | python cleaning_mysql_dump.py -d malignant > %s" %(path_to_sqlitedb, path_to_mysql_dump))

    print("Done: Sqlite data dumped")
    print("===================")

def remove_foreing_keys(path_to_mysql_dump):
    
    print("Starting: remove_foreing_keys")

    # open the source file and read it
    fh = file(path_to_mysql_dump, 'r')
    subject = fh.read()
    fh.close()

    # do the replace
    pattern = re.compile(r',\nFOREIGN KEY.*$',re.MULTILINE)
    result = pattern.sub("", subject)

    # write the file
    path_to_changed_mysql_dump = path_to_mysql_dump + '.copy'
    f_out = file(path_to_changed_mysql_dump, 'w')
    f_out.write(result)
    f_out.close()
    
    print("Done: Foreing keys removed")
    print("===================")

def add_key_length(path_to_mysql_dump):
    
    print("Starting: add_key_length")

    # open the source file and read it
    fh = file(path_to_mysql_dump, 'rw')
    subject = fh.read()
    fh.close()

    pattern = re.compile(r'PRIMARY KEY \((\`\w\`),(\`\w\`)\)')# "\d*,\d*"
    primary_keys = pattern.findall(subject)
    print(primary_keys)
    # todo: here we are changing all the rows with these names
    # ideally we should change just the rows of the corresponding table
    for key in primary_keys:
        pattern = re.compile(r'%s (TEXT),' %key)
        print(pattern.findall(subject))
        print(key)
        #subject = pattern.sub(" VARCHAR(200)", subject)

    # write the file
    path_to_changed_mysql_dump = path_to_mysql_dump + '.copy'
    f_out = file(path_to_changed_mysql_dump, 'w')
    f_out.write(subject)
    f_out.close()

    print("Done: Key constraint added")
    print("===================")

def edit_mysql_file(path_to_mysql_dump):
    path = path_to_mysql_dump
    sql_file = open(path,'rw')
    sql = sql_file.read()

    new_days.write(days)
    sql_file.close()

path_to_sqlitedb = ''
path_to_mysql_dump = ''


dump_sqlite_data(path_to_sqlitedb, path_to_mysql_dump)
remove_foreing_keys(path_to_mysql_dump)
add_key_length(path_to_mysql_dump + '.copy')
