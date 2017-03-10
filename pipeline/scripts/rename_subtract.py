#!/usr/bin/env python
"""
Script to rename groups of 10 sub-bands before the subtraction
"""
from __future__ import print_function
import os
import numpy as np
import sys
import subprocess
import re
from glob import glob

output_name_template = "L{}_SBgr{:03d}-10_uv.MS.pre-cal.ms"
output_name_template_tar = "L{}_SBgr{:03d}-10_uv.MS.pre-cal.ms.tar"
freq2band={115:0, 117:1, 119:2, 121:3, 123:4, 125:5, 127:6, 129:7, 
           131:8, 133:9, 135:10, 137:11, 139:12, 141:13, 143:14, 
           145:15, 147:16, 149:17, 151:18, 153:19, 154:20, 156:21, 
           158:22, 160:23, 162:24, 164:25, 166:26, 168:27, 170:28, 
           172:29, 174:30, 176:31, 180:32, 182:33, 184:34, 186:35}

def get_name(input_name):
    """
    Get the output name from the input name
    """
    L, freq_str = re.findall("^L(\d+)_.*_(\d+)MHz", input_name)[0]
    freq = int(freq_str)
    if input_name.endswith(".tar"):
        out = output_name_template_tar.format(L, freq2band[freq])
    else:
        out = output_name_template.format(L, freq2band[freq])
    return out

def rename_ms(ms, verbose=True):
    """
    Rename a single file
    """
    if not ms.endswith("/"):
        path, name = os.path.split(ms)
    else:
        path, name = os.path.split(ms[:-1])
    out_ms = get_name(name)
    if verbose:
        print("Rename {} to {}".format(name, out_ms))
    os.rename(ms, os.path.join(path, out_ms)) 

def rename_directory(directory, tar=False, verbose=True):
    """
    Rename all the relevant bands in a directory
    """
    mss = glob("{}/L*_SAP???_SB???_uv.MS_*_???MHz.pre-cal.*".format(directory))
    #print(mss)
    for ms in mss:
        rename_ms(ms, verbose=verbose)
        
           
if __name__ == "__main__":
    directory = str(sys.argv[1])
    rename_directory(directory)
    