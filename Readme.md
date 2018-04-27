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


## Convert amazon bucket tabular data into a mysql db

Use a python script.

- If needed, install the mysql modules for python

        pip install mysql-python

- Configure Python script

The python script reads its configuration from the environment.  These variables are required:

    export mysql_db=icare
    export directory_with_farsight_files=/Users/pbc/tmp
    export sql_dump=../honeyguide/db/farsight.sql

- Run the script by doing:

        python2.7 create_and_populate_table.py

## Get data from REDCap

We will use [QUAIL](git@github.com:ctsit/QUAIL.git) to get data from REDCap projects.

Note: Quail requires Python3.

- Install QUAIL's prerequisites

        git clone git@github.com:ctsit/cappy.git
        pip install -e cappy

- Install QUAIL as a python module by first cloning it in a local directory:

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

        export directory_for_redcap_data=`mktemp -d`
        quail install $directory_for_redcap_data
        export OLDDIR=`pwd`
        cd $directory_for_redcap_data
        quail redcap generate quail.conf.yaml "Malignant" 78JNMKDR346hhKJbj85DE4 http://redcap.test/redcap/api/
        quail redcap get_meta "Malignant"
        quail redcap get_data "Malignant"
        quail redcap gen_meta "Malignant"
        quail redcap gen_data "Malignant"
        quail redcap make_import_files "Malignant"
        export TODAYS_DATE=`date +%Y-%m-%d`
        cd $OLDDIR

- This will save the information for the REDCap project into a sqlite database in the directory `$directory_for_redcap_data/batches/Malignant/2018-03-19/data.db` were `2018-03-19` represents the current date.


## Convert sqlite db into mysql db

- The python script reads its configuration from the environment.  These variables are required:

        export mysql_db=icare
        export path_to_sqlitedb=$directory_for_redcap_data/batches/Malignant/$TODAYS_DATE/data.db
        export path_to_mysql_dump=~/git/honeyguide/db/malignant.sql

- Run script:

        python sqlite_to_mysql.py

- Erase the SQLite inputs
    
        rm -rf $directory_for_redcap_data


## Using honeyguide

- Go to https://github.com/marlycormar/honeyguide/tree/mysql, clone the repo locally, and checkout the mysql branch.

        git clone git@github.com:marlycormar/honeyguide.git
        cd honeyguide
        git checkout mysql

- Configure Honeyguide to load our data into a MySQL DB. Use fake.env as a template.  Copy it to ".env" and customize as needed.

        cp fake.env .env
        # edit .env

- Build and start honeyguide

        docker-compose up --build

- To access the web interface of redash go to [http://localhost:5000/](http://localhost:5000/).

- To add the datasource, you will need the container ip address. To get that, inspect the container and look for the `Gateway` ip address:

        docker inspect container_id

- To add a mysql datasource you will need the following information:

        Host: container_ip
        Port: 3306
        Password: password
        Database Name: redash

Notice that both the `malignant` and the `farsight` data sources will be loaded into the `icare` database in docker mysql instance.
