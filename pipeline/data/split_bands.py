from __future__ import print_function
import os
import re
try: # Python 3
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

def grouper(n, iterable, fillvalue=None):
    """
    Collect data into fixed-length chunks or blocks
    http://stackoverflow.com/questions/16289859/splitting-large-text-file-into-smaller-text-files-by-line-numbers-using-python
    """
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

def empirical_grouper(lines, n=40):
    """
    Empirical version of the grouper that considers the actual numbering
    of the bands
    """
    bands = {0:"", 1:"", 2:"", 3:"", 4:"", 
             5:"", 6:"", 7:"", 8:"", 9:""}
    for line in lines:
        sb = re.findall("SAP000_SB(\d\d\d)_uv", line)[0]
        sbi = int(sb)
        if sbi == 320:
            continue
        if sbi > 320:
            sbi = sbi-1
        print(line[:-1], sbi)
        band = int(sbi/n)
        bands[band] = bands[band] + line
    return bands
        

def main(path, data_file_name, n=40, g_iter=False):
    """
    Apply the grouper to the specified file
    """
    with open("{}/{}.txt".format(path, data_file_name), "r") as data_file:
        if g_iter:
            for i, g in enumerate(grouper(n, data_file, fillvalue='')):
                lines = list(g)
                lines[-1] = lines[-1][:-1] # Remove the new line from the last line
                with open("{}/{}-BAND{}.txt".format(path, data_file_name, i), 'w') as fout:
                    fout.writelines(lines)
        else:
            bands = empirical_grouper(data_file.readlines(), n=n)
            for i in range(10):
                with open("{}/{}-BAND{}.txt".format(path, data_file_name, i), 'w') as fout:
                    fout.write(bands[i])

if __name__ == "__main__":
    import sys
    data_file_name = "target"
    n = 40
    path = sys.argv[1]
    
    main(path, data_file_name, n=n)
    
    
    
            
