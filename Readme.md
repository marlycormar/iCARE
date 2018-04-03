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

- Useful commands:

    - Show the current buckets:

            s3 ls

    - List all the objects in a bucket:

            s3 ls s3://bucket_name

    - Exit the shell. Download all files into current directory:

            aws s3 sync s3://bucket_name .


## Create database

    CREATE DATABASE iCARE;

## Convert tabular data into a mysql db

Use a python script.

- If needed, install the mysql modules for python

        pip install mysql-python

- Configure Python script

The python script reads its configuration from the environment.  These variables are required:

    mysql_host
    mysql_user
    mysql_db
    directory_with_farsight_files

- Run the script by doing:

        python2 create_and_populate_table.py
