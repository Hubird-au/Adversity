#!/usr/bin/env python

#############################################################################
# Python script to add a checksum and date/time to an Adblock subscription. #
#                                                                           #
# To add a checksum to a subscription file, run the script like this:       #
#                                                                           #
#   python addChecksum.py subscription.txt                                  #
#                                                                           #
# Note: your subscription file should be saved in UTF-8 encoding, otherwise #
# the generated checksum might be incorrect.                                #
#############################################################################

import sys
import hashlib
import base64
import re
import datetime

def update_modified(contents):
    dt = datetime.datetime.today().strftime("%d %B %Y (%I:%M:%S %p)")
    return re.sub(r"(!\s*Updated\s*:\s*)[^\r\n]*(|(?:\r?\n))", "\\g<1>"+dt+"\\g<2>", contents, 1)

def checksum_data(data):
    # Remove all CR symbols and empty lines.
    ret = data.replace("\r", "")
    ret = re.sub(r"\n+", "\n", ret)

    # Calculate the base64 encoded md5 hash with trailing equal signs removed.
    m = hashlib.md5()
    m.update(ret)
    ret = base64.b64encode(m.digest()).rstrip("=")

    return ret

def usage():
    print(sys.argv[0] + " subscription.txt")

def main(fn):
    # Read the file.
    contents = ""
    with open(fn, "rb") as f:
        contents = f.read()

    # Regular expression used to find the checksum that's embedded in the file.
    rx = re.compile(r"^.*!\s*checksum[\s\-:]+([\w\+\/=]+).*(\r\n|\r|\n)?", re.M|re.I)

    # Get old checksum.
    ochk = rx.search(contents)
    if not ochk:
        return 0 # We don't touch files without existing checksums.
    old_checksum = ochk.group(1)

    # Remove the old checksum.
    contents = rx.sub("", contents)

    # Calculate a new checksum and determine if the file has been modified.
    new_checksum = checksum_data(contents)
    if old_checksum == new_checksum:
        return 0

    # Update the date and time.
    contents = update_modified(contents)

    # Recalculate the checksum as we've altered the date.
    new_checksum = checksum_data(contents)

    # Insert new checksum in file as the second line,
    contents = re.sub(r"(\r\n|\r|\n)", r"\1! Checksum: "+new_checksum+r"\1", contents, 1)

    # Write the new file.
    with open(fn, "w+b") as f:
        f.write(contents)

    print((fn+":").ljust(30) + ("Dated and checksummed".rjust(20)))

    return 0

if __name__=='__main__':
    # Parse command line.
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    try:
        sys.exit(main(sys.argv[1]))
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        sys.exit(1)
