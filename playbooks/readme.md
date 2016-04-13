Playbooks
=========

Compilation of playbooks that can be useful for the Astrocompute 
project.

* launch.yml - Test to launch an EC2 instance and install the LOFAR 
software. It will evolve to launch a complete cluster that will be used 
to process the data.
* lofar.yml - Is a simple playbook to test the role LOFAR which 
installs the LOFAR software (not used yet).

The inventory file contains the EC2 inventory scripts to maintain a 
dynamic inventory.

Roles
-----

Currently, there are six roles defined.

=== CASA
```casa```
Installs the version 4.2 of casapy.

=== LOFAR base
```lofar_base```
Installs the dependencies required by the releade 2.15 of LOFAR.

=== LOFAR
```lofar```
Installs the releade 2.15 of LOFAR.

=== Grid
```grid```
Installs some software required to download LOFAR data from the Grid.

=== Postgres8
```postgres8```
Install the PostgreSQL 8 database required by the Facet calibration pipeline.

=== WSClean
```wsclean```
Compiles and installs the WSClean imager.

TODO
----
* Define with a variable the version of casa
* Define with a variable the version of LOFAR
* Role to install the required version of Postgresql
* Role with just the dependencies to build and package LOFAR from 
scratch


Tips
----
* Ansible will use the system version of Python. It can fail if, for 
example the boto library is not installed system wide. To tell Ansible 
which Python interpeter to use, it is posible to add the following part 
to the hosts file: ansible_python_interpreter=/usr/local/bin/python
