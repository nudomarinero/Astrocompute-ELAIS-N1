#!/bin/bash
cd /tmp
tar xfj wsclean-2.4.tar.bz2
cd wsclean-2.4
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr ..
make
make install
cd /tmp
rm -rf wsclean-2.4*
