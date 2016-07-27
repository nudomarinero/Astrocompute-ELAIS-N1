#!/usr/bin/env python
"""
Script to correct the frequencies of MS 
observed during LOFAR cycle 0.
"""
from __future__ import print_function
import os
import numpy as np
from pyrap import tables
import argparse
from glob import glob
import re


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def main(ms):
    """
    Function to be called from the pipeline
    """
    correct_ms(ms)

def read_ms(ms):
    """
    Read the frequency center for each channel and the widths.
    Return also the frequency spacing
    """
    msfr = tables.table(os.path.join(ms, "SPECTRAL_WINDOW"), 
                        readonly=True)
    frequencies = msfr.getcol('CHAN_FREQ')[0]
    spacing = frequencies[1:]-frequencies[:-1]
    widths = msfr.getcol("CHAN_WIDTH")[0]
    msfr.close()
    return frequencies, spacing, widths

def write_ms(ms, freqs):
    """
    Write the frequency center for each channel and the widths.
    """
    msfr = tables.table(os.path.join(ms, "SPECTRAL_WINDOW"), 
                        readonly=False)
    # Check size of the freqs
    aux_freqs = np.expand_dims(freqs, axis=0)
    msfr.putcol('CHAN_FREQ', aux_freqs)

def get_central_freq(group, sb_per_group=10):
    """
    Get the central frequency of a group
    """
    mfreq = np.load(os.path.join(THIS_DIR, "mfreq.py")).astype("Float64")
    if sb_per_group % 2 == 0:
        return (mfreq[group*sb_per_group+sb_per_group//2-1]+
                mfreq[group*sb_per_group+sb_per_group//2])/2.
    else:
        return mfreq[group*sb_per_group+sb_per_group//2-1]

def compute_freqs(group, sb_per_group=10, channels_per_group=50):
    """
    Compute the even spacing of frequencies for a given group
    """
    central_freq = get_central_freq(group, sb_per_group=sb_per_group)
    
    # Heuristics for the channel positions
    if group < 30:
        central_freq_aux = get_central_freq(group+1, sb_per_group=sb_per_group)
    elif group == 32:
        ## WARNING
        central_freq_aux = get_central_freq(group-1, sb_per_group=sb_per_group)
    elif group == 33:
        central_freq_aux = get_central_freq(group+1, sb_per_group=sb_per_group)
    elif (group > 33) and (group <= 37):
        central_freq_aux = get_central_freq(group-1, sb_per_group=sb_per_group)
    else:
        ## ERROR
        central_freq_aux = get_central_freq(group-1, sb_per_group=sb_per_group)
    # Compute the channel step
    cstep = np.absolute(central_freq - central_freq_aux)/channels_per_group
    
    freq_comp = np.linspace(central_freq-(channels_per_group-0.5)*cstep, 
                           central_freq+(channels_per_group-0.5)*cstep, 
                           channels_per_group,
                           dtype="Float64")
    return freq_comp

def get_info(ms, read_cpg=True):
    """
    Get the group, number of sub-bands per group and number of channels 
    per groups for a given ms
    """
    msname = os.path.basename(ms)
    result = re.findall("_SBgr(\d+)-(\d+)_", msname)
    if result:
        group = int(result[0][0])
        sb_per_group = int(result[0][1])
    else:
        # ERROR
        group = None
        sb_per_group = None
    if read_cpg:
        frequencies, spacing, widths = read_ms(ms)
        channels_per_group = len(frequencies)
    else:
        channels_per_group = None
    return group, sb_per_group, channels_per_group

def show_ms(ms, machine_readable=False):
    frequencies, spacing, widths = read_ms(ms)
    print("Frequencies ({})".format(len(frequencies)))
    print(frequencies)
    print("Spacing")
    print(spacing)
    print("Widths")
    print(widths)
    # Detect the group name.
    # Compute the frequencies based on the group name.
    group, sb_per_group, channels_per_group = get_info(ms)
    freq_comp = compute_freqs(group, 
                              sb_per_group=sb_per_group, 
                              channels_per_group=channels_per_group)
    print("Computed frequencies")
    print(freq_comp)

def correct_ms(ms):
    """
    Correct the frequencies of a given MS.
    """
    frequencies, spacing, widths = read_ms(ms)
    # TODO: Correct


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check the frequency properties of MS files')
    parser.add_argument('-d', '--directory', action='store_true', help='directory with MS')
    parser.add_argument('-c', '--correct', action='store_true', help='Correct the frequencies of the MS')
    parser.add_argument('ms', help='MS or directory')
    args = parser.parse_args()
    # TODO: Check directory
    if args.directory:
        list_ms = glob(args.ms+"/*.ms")
        list_ms2 = glob(args.ms+"/*.MS")
        list_ms.extend(list_ms2)
        for ms in list_ms:
            if args.correct:
                correct_ms(ms)
            else:
                show_ms(ms)
    else:
        if args.correct:
            correct_ms(args.ms)
        else:
            show_ms(args.ms)