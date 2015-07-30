Packer
======

Files to pack the Amazon intances (AMIs) using packer (from 
https://www.packer.io/). 

Usage
-----

There are two definition files:
* lofar_node.json - with the CASA and LOFAR software
* lofar_head.json - Like a node but includes also the Grid utilities

To check if there are mistakes in the definition files:
```packer validate lofar_node.json```

To build the AMI:
```packer build lofar_node.json```

TODO
----
* Include the custom version of Postgres that is needed in the head 
node
* Check that all the Python dependencies for the final pipeline are 
installed

Tips
----
* It is fundamental to use the correct credentials with packer. 
Apparently, it will ignore the credentials stored in ~\.aws\credentials 
but will honour the environment variables with the API and secret keys. 
* If it is not possible to use the environmental variables, the 
credentials can be entered into the json file as "access_key": 
"YOUR KEY HERE" and "secret_key": "YOUR SECRET KEY HERE".