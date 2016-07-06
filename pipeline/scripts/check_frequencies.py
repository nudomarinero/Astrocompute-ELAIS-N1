#!/usr/bin/env python
"""
Script to check the frequencies of an MS.
"""
from __future__ import print_function
import os
import numpy as np
from pyrap import tables
import argparse
from glob import glob

def main(ms):
    """
    Function to be called from the pipeline
    """
    check_ms(ms)

def read_ms(ms):
    """
    Read the frequency center for each channel and the widths.
    Return also the frequency spacing
    """
    msfr = tables.table(os.path.join(ms, "SPECTRAL_WINDOW"), 
                        readonly=False)
    frequencies = msfr.getcol('CHAN_FREQ')[0]
    spacing = frequencies[1:]-frequencies[:-1]
    widths = msfr.getcol("CHAN_WIDTH")[0]
    return frequencies, spacing, widths

def check_ms(ms):
    frequencies, spacing, widths = read_ms(ms)
    print("Frequencies ({})".format(len(frequencies)))
    print(frequencies)
    print("Spacing")
    print(spacing)
    print("Widths")
    print(widths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check the frequency properties of MS files')
    parser.add_argument('-d', '--directory', action='store_true', help='directory with MS')
    parser.add_argument('ms', help='MS or directory')
    args = parser.parse_args()
    # TODO: Check directory
    if args.directory:
        list_ms = glob(args.ms+"/*.ms")
        list_ms2 = glob(args.ms+"/*.MS")
        list_ms.extend(list_ms2)
        for ms in list_ms:
            check_ms(ms)
    else:
        check_ms(args.ms)