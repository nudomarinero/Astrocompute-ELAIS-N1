Vagrant
=======

Test the role playbooks using vagrant.

Usage
-----

The provison file called by vagrant is provision.yml. This file have 
some includes to call the actual playbooks to be tested.

The playbooks in the main directory test the roles defined in 
../playbooks. There is also a directory with simple tests.

To start and provision a VM use:
```vagrant up```

If the VMm is up and you would like to run only Ansible use:
```vagrant provision```

To completely remove the VM use:
```vagrant destroy```
