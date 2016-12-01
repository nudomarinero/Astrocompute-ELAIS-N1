#!/bin/bash
cd /tmp/dysco
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr ..
make
make install
cd /tmp
rm -rf dysco
