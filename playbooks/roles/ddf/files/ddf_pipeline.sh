#!/bin/bash
cd /opt/ddf
#./ddf-pipeline/scripts/install.sh
export WD=`pwd`
git clone https://github.com/cyriltasse/SkyModel.git
git clone https://github.com/nudomarinero/killMS.git
cd killMS
git checkout lofar-stable
cd Predict
make
cd ../Array/Dot
make
cd ../../Gridder
make
cd $WD
git clone https://github.com/saopicc/DDFacet.git
cd DDFacet
git checkout lofar-stable
python setup.py build
cd $WD
sed -e "s|INSTALLDIR|$WD|" ddf-pipeline/misc/DDF.sh > init.sh
