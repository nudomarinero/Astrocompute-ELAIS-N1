#!/bin/bash
# Correct the frequencies of the data in the directory specified
python /home/ubuntu/astrocompute/pipeline/scripts/check_frequencies.py -c -w -r -t -d $1
