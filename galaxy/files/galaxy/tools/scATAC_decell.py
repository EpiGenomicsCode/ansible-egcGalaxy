#!/usr/bin/env python

import os
import sys
import collections
import optparse

def main():
    """ main function """
    parser = optparse.OptionParser(usage='%prog [-h] [-m Min reads per cell]',
                                   description='Parse individual cells from scATAC-seq data.')
    parser.add_option('-m',
                      dest="min",
                      help='Minimum number of reads',
                      type="int"
                      )

    if len(sys.argv) < 2:
        parser.print_help()
        exit('error: too few arguments')

    args = parser.parse_args()[0]
    min_reads = args.min

    os.mkdir('output')

    prev_barcode = ""
    instances = []
    heads = []
    for line in sys.stdin:
        if line.split()[0]=='@SQ' or line.split()[0]=='@PG':
            heads.append(line)
        else:
            cur_barcode = line.strip().split()[0].split(':')[0]
            if cur_barcode != prev_barcode:
                if(len(instances) >= min_reads) and prev_barcode != "":
                    with open(os.path.join('output', prev_barcode + '.sam'), 'w') as fout:
                        for elem in heads:
                            fout.write(elem)
                        for elem in instances:
                            fout.write(elem)
                prev_barcode = cur_barcode
                instances = []
                instances.append(line)
            else:
                instances.append(line)

if __name__ == '__main__':
    main()
