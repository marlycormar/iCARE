##  Install aws console

- Install aws:
    
        pip install aws-shell
        
- Run the shell:

        aws-shell
        
- If it fails with error `command not found`, add `~/.local/bin` to the current `$PATH` variable:
        
        export PATH=~/.local/bin:$PATH
        
and run `aws-shell` again.

- To exit the shell press `fn + F11`.