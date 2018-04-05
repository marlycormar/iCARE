##  Install aws console

- Install aws:

        pip install aws-shell

- Run the shell:

        aws-shell

- If it fails with error `command not found`, add `~/.local/bin` to the current `$PATH` variable:

        export PATH=~/.local/bin:$PATH

and run `aws-shell` again.

- To exit the shell press `fn + F10`.


## Configure aws

- Once inside the `aws-shell` run:

        configure

- You will be prompted to provide the following information:
    - AWS Access Key ID:
    - AWS Secret Access Key:
    - Default region name: us-east-1
    - Default output format:


- Test that you can enumerate the Farsight files in the bucket:

        s3 ls s3://fgs-ufh-farsight-results

- Exit the shell.


## Download all files from the amazon bucket

    cd $directory_with_farsight_files
    aws s3 sync s3://fgs-ufh-farsight-results .


## Create database if needed

    echo "CREATE DATABASE iCARE;" | mysql -u root


## Convert amazon bucket tabular data into a mysql db

Use a python script.

- If needed, install the mysql modules for python

        pip install mysql-python

- Configure Python script

The python script reads its configuration from the environment.  These variables are required:

    export mysql_host=localhost
    export mysql_user=root
    export mysql_password=password
    export mysql_db=iCARE
    export directory_with_farsight_files=/Users/pbc/tmp

- Run the script by doing:

        python2 create_and_populate_table.py
        
## Get data from REDCap

We will use [QUAIL](git@github.com:ctsit/QUAIL.git) to get data from REDCap projects.

- Install QUAIL as a python module by first clonning it in a local directory:

        git clone git@github.com:marlycormar/QUAIL.git
    
    and then installing it:

        pip install -e QUAIL
        
- General usage:

        quail install <root>
        quail redcap generate ( <quail.conf.yaml> <project_name> <token> <url> ) [-i --initialize]
        quail redcap get_meta (<project_name>) [ -q <quail.conf.yaml> ]
        quail redcap get_data (<project_name>) [ -q <quail.conf.yaml> ]
        quail redcap gen_meta (<project_name>) [ -q <quail.conf.yaml> ]
        quail redcap gen_data (<project_name>) [ -q <quail.conf.yaml> ]
        quail redcap make_import_files (<project_name>) [ -q <quail.conf.yaml> ]
        
- To run QUAIL:
        
        quail install $directory_for_redcap_data
        quail redcap generate quail.conf.yaml "Malignant" 78JNMKDR346hhKJbj85DE4 http://redcap.test/redcap/redcap_v8.2.0/api/
        quail redcap get_meta "Malignant"
        quail redcap get_data "Malignant"
        quail redcap gen_meta "Malignant"
        quail redcap gen_data "Malignant"
        quail redcap make_import_files "Malignant"
        
- This will save the information for the REDCap project into a sqlite database in the directory `$directory_for_redcap_data/batches/Malignant/2018-03-19/data.db` were `2018-03-19` represents the current date.

- To dump the sqlite database:

        sqlite3
        .open $directory_for_redcap_data/batches/Malignant/2018-03-19/data.db
        .output sqlite_dump.sql
        .dump
        .exit

## Convert sqlite db to postgres db

- Create `malignant` database:

        echo 'CREATE DATABASE malignant;' | psql postgres
        
- Convert sqlite db to postgress db:

        pgloader $directory_for_redcap_data/batches/Malignant/2018-03-19/data.db postgresql:///malignant
        
- Check that the convertion was succesfull:

        psql postgres
        \c malignant -- Change database to malignant
        \dt -- Show tables
        
        
## Conver sqlite db into mysql db

- The python script reads its configuration from the environment.  These variables are required:

        export mysql_user=root
        export mysql_password=password
        export mysql_db=malignant
        export path_to_sqlitedb=/Users/marlycormar/git/iCARE/main/dumps/data.db
        export path_to_mysql_dump=/Users/marlycormar/git/iCARE/main/dumps/malignant.sql

- Run script:

        python sqlite_to_mysql.py        





        

    
