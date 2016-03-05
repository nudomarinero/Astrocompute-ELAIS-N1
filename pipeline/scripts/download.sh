#!/bin/bash
# http://unix.stackexchange.com/questions/85194/how-to-download-an-archive-and-extract-it-without-saving-the-archive-to-disk
# Example: wget -qO- http://s3.amazonaws.com/lofar-elais-n1/L229391/L229391_SAP000_SB000_uv.MS.tar | tar xv -C ~/tmp
echo $1
wget -qO- $1 | tar x -C /mnt/scratch/data/raw