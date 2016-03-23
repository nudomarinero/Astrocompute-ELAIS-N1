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
import sys

def main(ms, group=5, edge_up=2, edge_down=2, force=False):
    """
    Function to be called from the pipeline
    """
    even_ms(ms, 
            group=group, 
            edge_up=edge_up, 
            edge_down=edge_down,
            force=force)

def even_ms(ms, group=5, edge_up=2, edge_down=2, force=False):
    """
    Replace the frequencies by an even spaced array.
    If the spacing is complex and known some additional parameters can
    be used to allow a better spacing.
    """
    msfr = tables.table(os.path.join(ms, "SPECTRAL_WINDOW"), 
                        readonly=False)
    frequencies = msfr.getcol('CHAN_FREQ')[0]
    
    if force or not check_assertion(frequencies):
        even_freqs_aux = get_even_frequencies(frequencies,
                                              group=group, 
                                              edge_up=edge_up, 
                                              edge_down=edge_down)
        # Update the data
        even_freqs = np.expand_dims(even_freqs_aux, axis=0)
        msfr.putcol('CHAN_FREQ', even_freqs)
        
    msfr.close()

def get_even_frequencies(frequencies, group=5, edge_up=2, edge_down=2, ch_per_sb=64):
    """
    Compute an array of evenly distributed frequencies.
    If the edge_up or edge_down are not 0, the estimated values of the
    upper and lower frequencies are computed.
    """
    n_freqs = len(frequencies)
    freq_up = frequencies[-1]
    freq_down = frequencies[0]
    if (edge_up != 0) or (edge_down != 0):
        n_channels_orig = n_freqs/group * ch_per_sb
        n_channels = n_channels_orig - edge_up - edge_down
        step_channel = (freq_up - freq_down)/float(n_channels-1)
        freq_up = freq_up + edge_up * step_channel
        freq_down = freq_down - edge_down * step_channel
    even_freqs_init = np.linspace(freq_down,
                                  freq_up,
                                  n_freqs)
    # Hack to pass the strong assertion
    step = even_freqs_init[1] - even_freqs_init[0]
    even_freqs_aux = np.arange(n_freqs)*step + freq_down
    return even_freqs_aux
    
def check_assertion(frequencies):
    """
    Check if the array of frequencies would pass the BBS assertion 
    """
    steps = frequencies[1:] - frequencies[:-1]
    return np.all(steps == steps[0])
    

if __name__ == "__main__":
    msname = str(sys.argv[1])
    