##  Install aws console

- Install aws:
    
        pip install aws-shell
        
- Run the shell:

        aws-shell
        
- If it fails with error `command not found`, add `~/.local/bin` to the current `$PATH` variable:
        
        export PATH=~/.local/bin:$PATH
        
and run `aws-shell` again.

- To exit the shell press `fn + F11`.


## Configure aws

- Once inside the `aws-shell` run:

        configure
        
- You will be prompted to provide the following information:
    - AWS Access Key ID: 
    - AWS Secret Access Key: 
    - Default region name:
    - Default output format:
    
- Useful commands:

    - Show the current buckets:

            s3 ls

    - List all the objects in a bucket:

            s3 ls s3://bucket_name

    - Exit the shell. Download all files into current directory:

            aws s3 sync s3://bucket_name .
    

## Convert tabular data into a mysql db

### v1.0.0
        
- Create database:

        CREATE DATABASE iCARE;
        
- Create table statement:

        csvsql --dialect mysql --snifflimit 100000 --table TABLE_NAME filename.csv > ../scripts/createtable.sql 

- Increase the size of columns:

        sed -i 's/VARCHAR([0-9]*)/VARCHAR(200)/g' ../scripts/createtable.sql

- Create table:

        cat ../scripts/createtable.sql | mysql -u root iCARE
        
- To now insert in the db, first check to which path the variable `secure_file_priv` is pointing to:

        SHOW VARIABLES LIKE "secure_file_priv";
        
- Modify it, if needed, by adding the following line to `/usr/local/etc/my.cnf`:

        secure-file-priv = "/Users/marlycormar/Google Drive/CTS-IT/Tasks/20180220/data/"

Note that if you do not change the path to the location containing your data, you will get the error:

        ERROR 1290 (HY000): The MySQL server is running with the --secure-file-priv option so it cannot execute this statement
        
- Now load the data into the created table:

        LOAD DATA INFILE '/Users/marlycormar/Google\ Drive/CTS-IT/Tasks/20180220/data/UFH_00078_001_S6_R1_001_FarsightAllVars_VI0209_587genelist.csv'
        INTO TABLE test FIELDS TERMINATED BY ',' ENCLOSED BY '"'
        LINES TERMINATED BY '\n' IGNORE 1 ROWS
        SET `id` = NULL, `study_id` = 'UFH_0007', `file_name` = 'UFH_00078_001_S6_R1_001_FarsightAllVars_VI0209_587genelist.csv';
        
- Got the following errors:

        ERROR 1406 (22001): Data too long for column 'column_name' at row 545
        
where `column_name`:

        ALTER TABLE farsight 
            MODIFY FATHMM_score VARCHAR(200),
            MODIFY FATHMM_pred VARCHAR(200),
            MODIFY CLIN_SIG VARCHAR(200),
            MODIFY PROVEAN_pred VARCHAR(200),
            MODIFY PROVEAN_score VARCHAR(200),
            MODIFY Consequence VARCHAR(200),
            MODIFY MutationTaster_score VARCHAR(200),
            MODIFY Alt VARCHAR(200),
            MODIFY pMut VARCHAR(200),
            MODIFY MutationTaster_pred VARCHAR(200),
            MODIFY Polyphen2_HVAR_score VARCHAR(200),
            MODIFY Amino_acids VARCHAR(200),
            MODIFY Codons VARCHAR(200),
            MODIFY Polyphen2_HDIV_score VARCHAR(200),
            MODIFY Polyphen2_HVAR_pred VARCHAR(200),
            MODIFY Uniprot_acc_Polyphen2 VARCHAR(200),
            MODIFY Polyphen2_HDIV_pred VARCHAR(200);

- Create indexes:

        CREATE INDEX chromosome_index
        ON test (ChromosomeNo);
        
        
### v1.0.1

Use a python script.

- Got error `No module named MySQLdb`. Installing mysql package for python:

        pip install mysql-python3
        
Note: python3 doesnt have this package =(. So use python2.

- Run the script by doing:

        python2 create_and_populate_table.py