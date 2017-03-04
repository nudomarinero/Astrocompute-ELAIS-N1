from __future__ import print_function
from glob import glob
import re
from subprocess import call

command_template = "python /home/ubuntu/astrocompute/pipeline/scripts/check_frequencies.py -c -t -r -w --group {} --sb-per-group 10 {}"

mss = glob("/mnt/scratch/data/cal/pre_facet_prefactor/L*_SAP000_SB???_uv.MS_*_???MHz.msdpppconcat")

base_group = int(re.findall("_SB(\d+)_", mss[0])[0])//10

mss.sort()
for i, ms in enumerate(mss):
    print(int(re.findall("_(\d+)MHz", ms)[0]))
    command = command_template.format(base_group+i, ms)
    print(command)
    call(command, shell=True)