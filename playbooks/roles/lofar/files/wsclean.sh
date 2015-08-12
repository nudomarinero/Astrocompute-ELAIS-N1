#!/bin/bash
cd /tmp
tar xfj wsclean-1.8.tar.bz2
cd wsclean-1.8
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr ..
make
make install
cd /tmp
rm -rf wsclean-1.8*
