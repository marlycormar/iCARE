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


## Convert tabular data into a mysql db

Use a python script.

- Got error `No module named MySQLdb`. Installing mysql package for python:

        pip install mysql-python3

Note: python3 doesnt have this package =(. So use python2.

- Run the script by doing:

        python2 create_and_populate_table.py