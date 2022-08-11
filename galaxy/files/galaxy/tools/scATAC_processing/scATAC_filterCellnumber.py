#!/usr/bin/env python

import sys
import optparse

def main():
    """ main function """
    parser = optparse.OptionParser(usage='%prog [-h] [-m Minimum Reads] [-f Barcode Frequency]',
                                   description='Filter BAM file, retaining cells with minimum number of associated reads.')
    parser.add_option('-m',
        dest="min_reads",
        help='Minimum reads to retain cell',
        type="int",
    )
    parser.add_option('-f',
        dest="freq",
        help='Barcode frequency'
    )

    if len(sys.argv) < 4:
        parser.print_help()
        exit('error: too few arguments')

    args = parser.parse_args()[0]
    min_cov = args.min_reads
    fname = args.freq

    barcode_list = []
    # load in the barcode
    with open(fname) as fin:
        for line in fin:
            [barcode, num] = line.split()
            num = int(num)
            if num >= min_cov: barcode_list.append(barcode)
    # iterate sam file
    for line in sys.stdin:
        # head of bam file
        if line[0] == '@':
            try:
                print(line,end='')
            except IOError:
                try:
                    sys.stdout.close()
                except IOError:
                    pass
                try:
                    sys.stderr.close()
                except IOError:
                    pass
            continue

        barcode_cur = line.split()[0].split(":")[0]
        if barcode_cur in barcode_list:
            try:
                print(line,end='')
            except IOError:
                try:
                    sys.stdout.close()
                except IOError:
                    pass
                try:
                    sys.stderr.close()
                except IOError:
                    pass


if __name__ == '__main__':
    main()
