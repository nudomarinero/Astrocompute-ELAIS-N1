#!/usr/bin/env python
"""
Script to unselect the MS files whose size is far from the median.

"""
from __future__ import print_function
import os
import numpy as np
import sys
import subprocess


def unselect(dir_size_list, threshold=0.001):
    """
    Select only the filenames with a deviation greater than 0.1% of the 
    value of the median
    """
    sizes = np.array([a[0] for a in dir_size_list])
    filenames = np.array([a[1] for a in dir_size_list])
    median_sizes = np.median(sizes)
    return filenames[np.abs(sizes - median_sizes) > (median_sizes*0.001)]

def list_filesizes_dir(directory):
    """
    Returns a list of tuples with the size and the name of the file
    """
    out = subprocess.check_output('du -s {}/*'.format(directory), shell=True)
    dulist = out.strip().split("\n")
    dir_size_list = [d.split("\t") for d in dulist]
    return dir_size_list
    
def move_unselected(filenames, suffix=".original"):
    """
    Move the selected filenames to a filename with an additional suffix
    """
    for f in filenames:
        #path, name = os.path.basename(f)
        os.rename(f, f+suffix)

def unselect_subbands(directory, threshold=0.001, suffix=".original"):
    """
    Main function to move the subbands
    """
    dir_size_list = list_filesizes_dir(directory)
    filenames = unselect(dir_size_list, threshold=threshold)
    print(filenames)

if __name__ == "__main__":
    directory = str(sys.argv[1])