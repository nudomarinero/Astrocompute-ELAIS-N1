#!/usr/bin/env python
"""
Script to rename groups of 10 sub-bands before the subtraction in S3
"""
from __future__ import print_function
import os
from subprocess import call, check_output
from rename_subtract import get_name

ls_template = "aws s3 ls s3://{bucket}/{ds}/data/"
mv_template = "aws s3 mv s3://{bucket}/{ds}/data/{inms} s3://{bucket}/{ds}/data/{outms}"

def rename_s3(ds, bucket="lofar-elais-n1-calibration"):
    """
    Rename the data files from the pre-facet calibration step for the
    dataset ds.
    """
    cmd_ls = ls_template.format(bucket=bucket, ds=ds)
    mss = check_output(cmd_ls, shell=True).split()[3::4]
    for ms in mss:
        try:
            outms = get_name(ms)
            cmd_mv = mv_template.format(bucket=bucket, ds=ds, inms=ms, outms=outms)
            print(cmd_mv)
            call(cmd_mv, shell=True)
        except IndexError:
            print("Ignore {}".format(ms))

if __name__ == "__main__":
    ds = "012"
    rename_s3(ds)
    
    
    

