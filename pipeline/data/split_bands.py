from __future__ import print_function
from itertools import izip_longest
import os

def grouper(n, iterable, fillvalue=None):
    """
    Collect data into fixed-length chunks or blocks
    http://stackoverflow.com/questions/16289859/splitting-large-text-file-into-smaller-text-files-by-line-numbers-using-python
    """
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def main(path, data_file_name, n=40):
    """
    Apply the grouper to the specified file
    """
    with open("{}/{}.txt".format(path, data_file_name), "r") as data_file:
        for i, g in enumerate(grouper(n, data_file, fillvalue='')):
            lines = list(g)
            lines[-1] = lines[-1][:-1] # Remove the new line from the last line
            with open("{}/{}-BAND{}.txt".format(path, data_file_name, i), 'w') as fout:
                fout.writelines(lines)

if __name__ == "__main__":
    import sys
    data_file_name = "target"
    n = 40
    path = sys.argv[1]
    
    main(path, data_file_name, n=n)
    
    
    
            