from __future__ import print_function
import pickle
import os
import sys

datasets = {
     0: "L133271",
     1: "L136068",
     2: "L136065",
     3: "L138664",
     4: "L138661",
     5: "L138658",
     6: "L139041",
     7: "L228621",
     8: "L228718",
     9: "L229064",
    10: "L229312",
    11: "L229387",
    12: "L229673",
    13: "L230461",
    14: "L230779",
    15: "L231211",
    16: "L231505",
    17: "L231647",
    18: "L232981",
    19: "L233804",
    }


def get_files():
    """
    Get the files stored in the public space
    """
    if os.path.exists("lofar-elais-n1_files.pckl"):
        print("Loading keys")
        return pickle.load(open("lofar-elais-n1_files.pckl", "rb"))
    else:
        from boto.s3.connection import S3Connection
        conn = S3Connection()
        mybucket = conn.get_bucket('lofar-elais-n1')
        keys = mybucket.list()
        print("Keys retrieved")
        names = [key.name for key in keys]
        print("Saving keys")
        pickle.dump(names, open("lofar-elais-n1_files.pckl", "wb"))
        return names

def filter_names(n, names):
    """
    Get the files corresponding to the central beam of the given 
    dataset
    """
    out = []
    for name in names:
        if name.startswith(datasets[n]) and ("SAP000" in name):
            out.append(name)
    return out

def output(selected_names, n):
    dataset = "{:03d}".format(n)
    if not os.path.exists("{}/target.txt".format(dataset)):
        if not os.path.exists(dataset):
            os.makedirs(dataset)
        with open("{}/target.txt".format(dataset), "w") as out:
            for name in selected_names:
                out.write("http://s3.amazonaws.com/lofar-elais-n1/{}\n".format(name))

if __name__ == "__main__":
    names = get_files()
    
    path = sys.argv[1]
    ipath = int(path)
    
    selected_names = filter_names(ipath, names)
    output(selected_names, ipath)

    
    
