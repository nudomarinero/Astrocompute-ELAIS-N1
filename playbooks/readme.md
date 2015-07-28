Playbooks
=========

Compilation of playbooks that can be useful for the Astrocompute 
project.

* launch.yml - Test to launch an EC2 instance and install the LOFAR 
software. It will evolve to launch a complete cluster that will be used 
to process the data.
* lofar.yml - Is a simple playbook to test the role LOFAR which 
installs the LOFAR software (not used yet).

Roles
-----
The roles to be defined are related to the installation of LOFAR 
software and the dependencies needed to gather the data.


Tips
----
* Ansible will use the system version of Python. It can fail if, for 
example the boto library is not installed system wide. To tell Ansible 
which Python interpeter to use, it is posible to add the following part 
to the hosts file: ansible_python_interpreter=/usr/local/bin/python
