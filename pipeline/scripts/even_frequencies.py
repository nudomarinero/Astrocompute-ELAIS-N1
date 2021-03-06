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
import argparse

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


def show_ms(ms, group=5, edge_up=2, edge_down=2, force=False):
    """
    Show the frequencies by an even spaced array.
    If the spacing is complex and known some additional parameters can
    be used to allow a better spacing.
    """
    msfr = tables.table(os.path.join(ms, "SPECTRAL_WINDOW"), 
                        readonly=True)
    frequencies = msfr.getcol('CHAN_FREQ')[0]
    even_freqs_aux = get_even_frequencies(frequencies,
                                          group=group, 
                                          edge_up=edge_up, 
                                          edge_down=edge_down)
    print(frequencies)
    print(even_freqs_aux)
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
    parser = argparse.ArgumentParser(description='Even the frequency in a MS file')
    parser.add_argument('-f', '--force', action='store_true', help='Force update')
    parser.add_argument('-n', '--dry-run', action='store_true', help='Just show the results')
    parser.add_argument('-g', '--group', type=int, default=5, help='Number of channels per sb (default: 5)')
    parser.add_argument('-d', '--edge-down', type=int, default=2, help='Channels removed from the lower edge (default: 2)')
    parser.add_argument('-u', '--edge-up', type=int, default=2, help='Channels removed from the upper edge (default: 2)')
    parser.add_argument('ms', help='MS or directory')
    args = parser.parse_args()
    
    if args.dry_run:
        show_ms(args.ms, 
                group=args.group, 
                edge_up=args.edge_up, 
                edge_down=args.edge_down)
    else:
        even_ms(args.ms, 
                group=args.group, 
                edge_up=args.edge_up, 
                edge_down=args.edge_down,
                force=args.force)