#!/usr/bin/env python
"""
Script to check the frequencies of an MS.
"""
from __future__ import print_function
import os
import numpy as np
from pyrap import tables
import sys

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
    msname = str(sys.argv[1])
    check_ms(msname)