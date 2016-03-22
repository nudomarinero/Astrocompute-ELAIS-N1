#!/usr/bin/env python
"""
Script to change the frequencies of an MS to make them even.
This is a dangerous script that you should only use if you know what 
you are doing
"""
from __future__ import print_function
import os
import numpy as np
from pyrap import tables

def main(ms):
    """
    Function to be called from the pipeline
    """
    even_ms(ms)

def even_ms(ms):
    """
    Replace the frequencies by an even spaced array
    """
    freq_table = os.path.join(ms, "SPECTRAL_WINDOW")
    # TODO: Check if the table exists
    msfr = tables.table(freq_table, readonly=False)
    frequencies = msfr.getcol('CHAN_FREQ')[0]
    n_freqs = len(frequencies)
    even_freqs_init = np.linspace(frequencies[0],
                                  frequencies[-1],
                                  n_freqs,
                                  dtype="float64")
    # Dirty hack to pass the strong assertion
    step = even_freqs_init[1] - even_freqs_init[0]
    even_freqs_aux = np.arange(n_freqs)*step + even_freqs_init[0]
    
    # TODO: Check the deviation
    even_freqs = np.expand_dims(even_freqs_init, axis=0)
    msfr.putcol('CHAN_FREQ', even_freqs)
    msfr.close()

if __name__ == "__main__":
    msname = str(sys.argv[1])
    