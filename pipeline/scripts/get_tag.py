"""
Get the value of a tag
"""
from __future__ import print_function
from get_band import get_tag
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get the value of an EC2 tag')
    parser.add_argument('tag', help='Tag to get')
    args = parser.parse_args()
    
    print(get_tag(args.tag))
    

