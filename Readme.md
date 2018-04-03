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


## Download all files

    cd $directory_with_farsight_files
    aws s3 sync s3://fgs-ufh-farsight-results .


## Create database if needed

    echo "CREATE DATABASE iCARE;" | mysql -u root

## Convert tabular data into a mysql db

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
