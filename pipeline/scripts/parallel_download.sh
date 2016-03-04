#!/bin/bash
cat $1 | xargs -n 1 -P 16 /home/ubuntu/astrocompute/pipeline/scripts/download.sh