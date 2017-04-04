from __future__ import print_function
from sh import aws

# Get list of datasets of lofar-elais-n1
base_html = "http://s3.amazonaws.com/lofar-elais-n1/{}"
header = """---
layout: default
title: ELAIS-N1 public data
---

# ELAIS-N1 public data

The ELAIS-N1 data presented here is publicly available for download:
"""
with open("../data.md", "w") as out:
    out.write(header)
    for line in aws(["s3", "ls", "--recursive", "s3://lofar-elais-n1/"], _iter=True):
        l = line.strip().split()
        print(l[-1])
        link = base_html.format(l[-1])
        name = l[-1].split("/")[-1]
        out.write("* [{}]({}) size: {}\n".format(name, link, l[-2]))

    
