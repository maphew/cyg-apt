#!/usr/bin/python
import pdb
import argparse
import os
import re
import sys
from path import path


def hasfiles(to_check):
    files = path.walkfiles(path(to_check))
    fl = list(files)
    if fl:
        print "Files exist: "
        for f in fl:
            print f
        return 1
    else:
        return 0
    
def main():
    parser =  argparse.ArgumentParser(description = "Checks a directory recursively for any files, returns true if any files exist.")
    parser.add_argument("to_check",\
        help="Directory to check for files", metavar="DIR")

    #pdb.set_trace()
    options = parser.parse_args()
    hasfiles(options.to_check)

    
    
if __name__ == "__main__":
    main()
    
