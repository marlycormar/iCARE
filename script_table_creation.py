import csv
import MySQLdb
import os

# read configuration from environment
mysql_db = os.environ['mysql_db']
directory = os.environ['directory_with_farsight_files']
sql_dump = os.environ['sql_dump']
table_name = 'farsight'
