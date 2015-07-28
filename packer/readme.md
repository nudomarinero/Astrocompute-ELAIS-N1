Packer
======

Files to pack the Amazon intances (AMIs) using packer (from 
https://www.packer.io/). 

The lofar.yml is a simple complete playbook that is used to install the
LOFAR software. We will use a role in the future.

Tips
----
* It is fundamental to use the correct credentials with packer. 
Apparently, it will ignore the credentials stored in ~\.aws\credentials 
but will honour the environment variables with the API and secret keys. 
* If it is not possible to use the environmental variables, the 
credentials can be entered into the json file as "access_key": 
"YOUR KEY HERE" and "secret_key": "YOUR SECRET KEY HERE".