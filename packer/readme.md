Packer
======

Files to pack the Amazon intances (AMIs) using packer (from 
https://www.packer.io/). 

Usage
-----

The definition file is ```lofar.json``` and includes the CASA, the LOFAR 
software and also the Grid utilities.

To check if there are mistakes in the definition file:
```packer validate lofar.json```

To build the AMI:
```packer build lofar.json```

Tips
----
* It is fundamental to use the correct credentials with packer. 
Apparently, it will ignore the credentials stored in ~\.aws\credentials 
but will honour the environment variables with the API and secret keys. 
* If it is not possible to use the environmental variables, the 
credentials can be entered into the json file as "access_key": 
"YOUR KEY HERE" and "secret_key": "YOUR SECRET KEY HERE".