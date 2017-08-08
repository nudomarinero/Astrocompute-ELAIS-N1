#!/usr/bin/env python
import os

### Configuration
config = {
    "source_dir" : "/vagrant/package_LOFAR",
    "version" : "2.21",
    "release" : "2_21",
    "trunk" : False,
    "ext_version" : "2.21.100",
    "pkgrelease" : "1xenial",
    "platform" : "amd64"
    }

patches = [
#    {"file": "CEP/DP3/DPPP/include/DPPP/CMakeLists.txt", 
#     "patch": "DPPP_include.patch"},
    {"file": "LCS/MessageBus/src/CMakeLists.txt", 
     "patch": "LCS_MessageBus_cpp11.patch"},
    {"file": "CEP/DP3/AOFlagger/src/CMakeLists.txt", 
     "patch": "AOFlagger_cpp11.patch"},
    ]
###

if "release" not in config.keys():
    config["release"] = config["version"].replace(".", "_")
    
if "ext_version" not in config.keys():
    config["ext_version"] = config["version"]+".100"

if config.get("trunk", False):
    config["svn"] = "https://svn.astron.nl/LOFAR/trunk"
else:
    config["svn"] = "https://svn.astron.nl/LOFAR/branches/LOFAR-Release-{release}".format(**config)
    
## Generate patches lines
if patches:
    lines = ""
    for patch in patches:
        patch["source_dir"] = config["source_dir"]
        lines += "patch -b {file} {source_dir}/patches/{patch}\n".format(**patch)
    config["patches"] = lines
else:
    config["patches"] = ""


template_bash = """
#!/bin/bash

cd
svn co --username "lofar" --password "M_OKZZJBTNuI" --non-interactive \
{svn} LOFAR
cd LOFAR

{patches}

mkdir -p build/gnu_opt; cd build/gnu_opt


mkdir /opt/LofIm-{release}
cmake ../.. \
 -DBUILD_SHARED_LIBS=ON \
 -DCMAKE_INSTALL_PREFIX=/opt/LofIm-{release} \
 -DUSE_OPENMP=ON \
 -DF2PY_FCOMPILER=gnu95 \
 -DUSE_QPID=OFF \
 -DBUILD_TESTING=OFF \
 -DBUILD_PACKAGES=Offline
make


# Prepare dependencies for checkinstall
sudo apt-get install -y checkinstall

cp {source_dir}/description-pak .
cp {source_dir}/postinstall-pak .
chmod +x postinstall-pak

sudo checkinstall -D --nodoc --install=no \
--requires="fftw3-dev,libreadline-dev,libxml2-dev,libpng-dev,libblas-dev,\
liblapack-dev,libboost-all-dev,zlib1g-dev,libfreetype6-dev,libncurses5-dev,\
libatlas-base-dev,wcslib-dev,hdf5-tools,libhdf5-dev,libhdf5-serial-dev,\
libzmq-dev,liblzo2-dev,valgrind,libssh2-1-dev,libblitz0-dev,libpqxx3-dev,\
libpq-dev,libunittest++-dev,liblog4cplus-dev,libgsl-dev,xvfb,casacore-tools,\
casacore-dev,python-casacore,aoflagger,libcasasynthesis1,libarmadillo-dev" \
--maintainer="Jose Sabater Montes\ \<jsm@iaa.es\>" \
--pkgname=lofar --pkgversion={ext_version} --pkgrelease={pkgrelease} \
--exclude=/home --showinstall=no -y --backup=no \
make install

# Copy the result back
cp lofar_{ext_version}-{pkgrelease}_{platform}.deb {source_dir}/lofar_{version}-{pkgrelease}_{platform}.deb

cd
#sudo rm -rf LOFAR
"""

template_postinstall = """
#!/bin/bash
# Remove symbolic link
if [ -h /opt/LofIm ]; then
    rm /opt/LofIm
fi
# Create symbolic link
if [ ! -e /opt/LofIm ]; then
    ln -s /opt/LofIm-{release} /opt/LofIm
fi
"""

template_description = """
LOFAR software compilation. Release {ext_version}.
"""

file_template = {
    "description-pak" : template_description,
    "postinstall-pak" : template_postinstall,
    "package.sh" : template_bash,
    }


if __name__ == "__main__":
    # Create files
    for fname, template in file_template.iteritems():
        with open(os.path.join(config["source_dir"], fname), "wb") as f:
            f.write(template.format(**config))
    
    # Execute files
    bash_file = os.path.join(config["source_dir"], "package.sh")
    os.chmod(bash_file, 755)
    command = ". "+bash_file
    print command
    os.system(command)