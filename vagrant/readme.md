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

When the base box, in this case Ubuntu 14.04 LTS, gets outdated, it 
is possible to update it with:
```vagrant box update```

Build LOFAR packages
--------------------
It is possible to build a debian package containing the LOFAR release
using vagrant.

At the moment the release number has to be manually edited in the file 
```package_LOFAR.py``` that is in the directory ```package_LOFAR```. 
The output .deb package will be located in this directory at the end.

To compile the package the following command has to be run:
```VAGRANT_VAGRANTFILE=Vagrantfile.build vagrant up```