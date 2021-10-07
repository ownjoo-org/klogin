# klogin
simple script to automate kerberos commands for realm authentication with OTP

you must create a file, props.py, that contains the variables that hold the strings appropriate for your environment:
ie. 
```cache_regex = 'Ticket cache: (.*)'
realm = 'MY.REALM.COM'
local_dir = "C:\\Program Files\\cygwin\\bin\\"
expected_cache = 'FILE:/tmp/krb5cc_abcdefg'
```
