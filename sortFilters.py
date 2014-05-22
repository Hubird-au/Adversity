#!/usr/bin/env python

#############################################################################
# Python script to sort an Adblock subscription.                            #
#                                                                           #
# Usage:                                                                    #
#   python sortFilters.py [-a] subscription.txt                             #
#                                                                           #
# The -a option uses an alternate sorting algorithm.                        #
#############################################################################

import sys
import re

class section(object):
    def __init__(self):
        self.comments = []
        self.filters = []

    cmt_txt = re.compile(r"(?:\[.*\])|(?:!.*)") # .txt
    cmt_ini = re.compile(r"(?:\[.*\])|(?:#.*)") # .ini
    def read_line(self, line, is_text):
        cm = section.cmt_txt.match(line) if is_text \
             else section.cmt_ini.match(line)
        if self.filters or not cm:
            if cm:
                # filters is not empty and we've just ran into a comment.
                # Return False to signal that this comment belongs in the
                # next section.
                return False
            self.filters.append(line)
            return True
        else:
            self.comments.append(line)
            return True

    def sort(self, alternate_sort):
        if alternate_sort:
            self.filters.sort(section.alternate_compare)
        else:
            self.filters.sort(section.compare)

    def __str__(self):
        ret = "";
        for c in self.comments:
            ret = ret + c
        for f in self.filters:
            ret = ret + f
        return ret

    # Compare lower case versions of the strings.
    # If the lower case versions compare the same return the result
    # comparing the unaltered strings.
    @staticmethod
    def compare(l, r):
        res = cmp(l.lower(), r.lower())
        if res == 0:
            return cmp(l, r)
        return res

    # When comparing two element hiding rules compares first using the
    # CSS portion and if these are equal falls back to the domain portion
    # (the actual comparison is done using the normal compare function).
    # If one rule is an element hiding rule and the other isn't the
    # element hiding rule comes first. Other cases compare normally.
    elem_hide_rex = re.compile(r"(.*)##(.*)")
    @staticmethod
    def alternate_compare(l, r):
        lm = section.elem_hide_rex.match(l)
        rm = section.elem_hide_rex.match(r)

        if lm and rm:
            comp_g2 = section.compare(lm.group(2), rm.group(2))
            if comp_g2 != 0:
                return comp_g2
            else:
                return section.compare(lm.group(1), rm.group(1))
        elif lm and not rm:
            # Put element hiding rules first.
            return -1;
        elif not lm and rm:
            # Put element hiding rules first.
            return 1;
        else:
            return section.compare(l, r)

rx_empty_line = re.compile(r"\s*(?:\x0d\x0a)|\x0a|\x0d")
def is_empty_line(l):
    return rx_empty_line.match(l) != None

def usage():
    print(sys.argv[0] + " [-a] subscription.txt")

def main(fn, alt_sort=False):
    # Determine the file type.
    is_text = True
    if fn[-4:].lower() == ".ini":
        is_text = False

    section_list = []
    s = section()

    with open(fn, "rb") as f:
        for line in f:
            # Skip empty lines.
            if is_empty_line(line):
                continue

            ok = s.read_line(line, is_text)
            if not ok:
                # We got a comment while processing with a non-empty
                # filter list. This means we need to start a new section.
                section_list.append(s) # Save the current section
                s = section()
                s.read_line(line, is_text)
        # Since we append a section above only when we need to start a new
        # one we have to make sure to add the final one.
        section_list.append(s)

    # Sort the filters.
    for s in section_list:
        s.sort(alt_sort)

    # Update the file.
    with open(fn, "w+b") as f:
        for s in section_list:
            f.write(str(s))

    print((fn+":").ljust(30) + ("Sorted".rjust(20)))

    return 0

if __name__=='__main__':
    # Parse the command line.
    if len(sys.argv)!=2 and len(sys.argv)!=3:
        usage()
        sys.exit(1)

    fn = ""
    alt_sort = False
    if sys.argv[1]=="-a":
        if len(sys.argv) != 3:
            usage()
            sys.exit(1)
        alt_sort = True
        fn = sys.argv[2]
    else:
        fn = sys.argv[1]

    # Execute the main function and handle errors.
    try:
        sys.exit(main(fn, alt_sort))
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        sys.exit(1)
