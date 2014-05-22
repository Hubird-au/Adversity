#!/usr/bin/env python

#############################################################################
# Python script to join multiple Adblock subscription files together        #
#                                                                           #
# Usage:                                                                    #
#     python join.py <source 1><source 2>...<source n><destination>         #
#                                                                           #
#############################################################################

import sys
import re

# The regular expression we use to extract checksums.
rx_checksum = re.compile(r"^.*!\s*checksum[\s\-:]+([\w\+\/=]+).*(\r\n|\r|\n)?", re.I)

# To extract the updated line.
rx_updated = re.compile(r"^.*!\s*updated[\s\-:]+.*(?:\r\n|\r|\n)?", re.I)

# Extract the first checksum and updated date comment lines from a file.
def extract_checksum_and_updated(fn):
    chk = ""
    cmt = ""
    with open(fn, "rb") as f:
        for line in f:
            if not chk:
                m = rx_checksum.match(line)
                if m:
                    chk = m.group(0)
            if not cmt:
                m = rx_updated.match(line)
                if m:
                    cmt = m.group(0)
            if chk and cmt:
                break

    return (chk, cmt)

class line_filter(object):
    def __init__(self, title, checksum, updated):
        self.got_version = False
        self.got_checksum = False
        self.checksum = checksum
        self.got_updated = False
        self.updated = updated
        self.got_title = False
        self.title = title
        self.ending = ""

    rx_version = re.compile(r"\s*\[.*\]\s*(?:\r\n|\r|\n)?")
    rx_ending = re.compile(".*(\r\n|\r|\n)")
    rx_title = re.compile(r"!\s*title[\s\-:]+.*(?:\r\n|\r|\n)?", re.I)

    def filter(self, line):
        if not self.ending:
            em = line_filter.rx_ending.match(line)
            if em:
                self.ending = em.group(1)

        # Only the first Adblock version line is preserved.
        if line_filter.rx_version.match(line):
            if not self.got_version:
                self.got_version = True
                return line
            else:
                return ""

        # The first checksum line up updated, the rest are removed.
        if self.checksum and rx_checksum.match(line):
            if not self.got_checksum:
                self.got_checksum = True
                return self.checksum
            else:
                return ""

        # The first updated line is updated, the rest are preserved.
        if not self.got_updated:
            if rx_updated.match(line):
                self.got_updated = True
                return self.updated

        # Keep the first title line (but with our title), discard the rest.
        if self.rx_title.match(line):
            if self.got_title:
                return ""
            else:
                self.got_title = True
                return "! Title: " + self.title + self.ending

        return line

    def line_ending(self):
        return self.ending


def main(title, sources, destination):
    (checksum, updated) = extract_checksum_and_updated(destination)

    lf = line_filter(title, checksum, updated)

    with open(destination, "w+b") as dst_file:
        for src in sources:
            with open(src, "rb") as src_file:
                for line in src_file:
                    dst_file.write(lf.filter(line))
            dst_file.write(lf.line_ending())

    print((destination+":").ljust(30) + ("Joined".rjust(20)))

    return 0

def usage():
    print(sys.argv[0] + " <title><source 1><source 2>...<source n><destination>")
    print("At least two source files are needed.")

if __name__=='__main__':
    # Parse the command line.
    if len(sys.argv) <= 4:
        usage()
        sys.exit(1)
    title = sys.argv[1]
    sources = sys.argv[2:-1]
    destination = sys.argv[-1:][0]

    # Call the main function.
    try:
        sys.exit(main(title, sources, destination))
    except IOError as e:
        print("I/O error in \"{0}\"({1}): {2}".format(e.filename, e.errno, e.strerror))
