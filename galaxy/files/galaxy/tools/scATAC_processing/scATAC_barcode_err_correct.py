#!/usr/bin/env python

import sys
import collections
import os
import optparse

def min_dist(s, sl):
    """ return the string with min edit distance """
    ss = sl[:]
    if len(s) == 0: sys.exit("error(min_dist): inquiry string has length 0")
    if len(ss) == 0: sys.exit("error(min_dist): ref string lib has 0 elements")
    if ([len(s) == len(sj) for sj in ss].count(False) > 0): sys.exit("error(min_dist): different string length")
    dists = [[a == b for (a,b) in zip(s, sj)].count(False) for sj in ss]
    min_value = min(dists)
    min_index = dists.index(min(dists))
    min_s = ss[min_index]

    # find the 2nd min element in the list
    del dists[min_index]
    del ss[min_index]

    min_value2 = min(dists)
    min_index2 = dists.index(min(dists))
    min_s2 = ss[min_index2]
    return (min_s, min_value, min_s2, min_value2)

def main():
    """ main function """
    parser = optparse.OptionParser(usage='%prog [-h] [-m mismatches allowed] [-a r7_ATAC] [-b i7_ATAC] [-c i5_ATAC] [-d r5_ATAC] [-o Output Barcode ID]',
                                   description='Barcode error correction single-cell ATAC-seq allowing mismatch.')
    parser.add_option('-m',
        dest="mismatch",
        help='Mismatches allowed',
        type="int",
    )
    parser.add_option('-a',
        dest="r7",
        help='r7 Barcodes'
    )
    parser.add_option('-b',
        dest="i7",
        help='i7 Barcodes'
    )
    parser.add_option('-c',
        dest="i5",
        help='i5 Barcodes'
    )
    parser.add_option('-d',
        dest="r5",
        help='r5 Barcodes'
    )
    parser.add_option('-o',
        dest="output",
        help='Uniq barcode list'
    )

    if len(sys.argv) < 12:
        parser.print_help()
        exit('error: too few arguments')

    args = parser.parse_args()[0]
    max_mm = args.mismatch
    r7_ATAC = args.r7
    i7_ATAC = args.i7
    i5_ATAC = args.i5
    r5_ATAC = args.r5
    output = args.output

    table_r7 = [x.strip() for x in open(r7_ATAC).readlines()]
    table_i7 = [x.strip() for x in open(i7_ATAC).readlines()]
    table_i5 = [x.strip() for x in open(i5_ATAC).readlines()]
    table_r5 = [x.strip() for x in open(r5_ATAC).readlines()]

    if len(table_r7) == 0: sys.exit("error(main): r7 table has 0 elements")
    if len(table_i7) == 0: sys.exit("error(main): i7 table has 0 elements")
    if len(table_r5) == 0: sys.exit("error(main): r5 table has 0 elements")
    if len(table_i5) == 0: sys.exit("error(main): i5 table has 0 elements")

    uniqBarcode = set()

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

        barcode = line.split()[0].split(':')[0]
        cur_r7 = barcode[:8]
        cur_i7 = barcode[8:16]
        cur_i5 = barcode[16:24]
        cur_r5 = barcode[24:]
        # skip this read if barcode has mismatch with r5 or r7
        if not cur_r7 in table_r7:  # if not perfectly matched
            (opt_match, num_mm, opt_match2, num_mm2) = min_dist(cur_r7, table_r7)
            if num_mm <= max_mm and abs(num_mm2 - num_mm) > 1:
                cur_r7 = opt_match
            else:
                continue

        if not cur_r5 in table_r5:
           (opt_match, num_mm, opt_match2, num_mm2) = min_dist(cur_r5, table_r5)
           if num_mm <= max_mm and abs(num_mm2 - num_mm) > 1:
               cur_r5 = opt_match
           else:
               continue


        if cur_i5 not in table_i5:
            (opt_match, num_mm, opt_match2, num_mm2) = min_dist(cur_i5, table_i5)
            if num_mm <= max_mm and abs(num_mm2 - num_mm) > 1:
                cur_i5 = opt_match
            else:
                continue

        if cur_i7 not in table_i7:
            (opt_match, num_mm, opt_match2, num_mm2) = min_dist(cur_i7, table_i7)
            if num_mm <= max_mm and abs(num_mm2 - num_mm) > 1:
                cur_i7 = opt_match
            else:
                continue
        # new barcode
        barcode = cur_r7 + cur_i7 + cur_i5 + cur_r5
        uniqBarcode.add(barcode)
        try:
            print(barcode + line[len(barcode):],end='')
        except IOError:
            try:
                sys.stdout.close()
            except IOError:
                pass
            try:
                sys.stderr.close()
            except IOError:
                pass

    with open(output, 'w') as fout:
        for elem in uniqBarcode:
            fout.write(elem + "\n")

if __name__ == '__main__':
    main()
