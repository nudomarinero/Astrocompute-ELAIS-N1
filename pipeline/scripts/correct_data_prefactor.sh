#!/bin/bash
# Correct the frequencies of the data in the directory specified
for i in $(ls -1d ${1}*.${2:-dppp}); 
do
python /home/ubuntu/astrocompute/pipeline/scripts/check_frequencies.py -c -w -r -t $i;
done
