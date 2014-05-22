#!/usr/bin/env python

#############################################################################
# Python script to checksum, sort, commit and push changes.                 #
#                                                                           #
# Usage:                                                                    #
#     [python] publish.py                                                   #
#                                                                           #
#############################################################################

import sortFilters
import addChecksum
import join
import subprocess
import sys
import glob

# List of files to process. Add additional entries here.
files = ["Adversity.txt", "Antisocial.txt", "Extreme-Measures.txt"]

def process_file(fn):
    sortFilters.main(fn)
    addChecksum.main(fn)

def create_combined():
    combined_fn = "Adversity-Combined.txt"
    join.main("Adversity-Combined", glob.glob("*.txt"), combined_fn)
    process_file(combined_fn)

def pull():
    print("---Pulling---")
    cmd = ["hg", "pull", "-u"]
    res = subprocess.call(cmd)
    if res!=0:
        return 1
    print("---Done---")
    return 0

def checkin(comment=None):
    print("---Committing---")
    cmd = ["hg", "commit"]
    if comment:
        cmd += ["-m", comment]
    res = subprocess.call(cmd)
    if res!=0:
        return 1
    print("---Done---")

    print("---push---")
    res = subprocess.call(["hg", "push"])
    if res!=0:
        return 1
    print("---Done---")

    print()
    subprocess.call(["hg", "heads"])

    return 0

def main():
    res = pull()
    if res!=0:
        return res

    for f in files:
        process_file(f)

    create_combined()

    res = checkin(" ".join(sys.argv[1:]))
    if res!=0:
        return res

    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        sys.exit(1)
