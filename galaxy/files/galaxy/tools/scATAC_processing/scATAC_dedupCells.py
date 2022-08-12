#!/usr/bin/env python

import os
import sys
import collections
import optparse
import pysam

def main():
    """ main function """
    parser = optparse.OptionParser(usage='%prog [-h] [-m Min reads per cell] [-o Output BAM file]',
                                   description='Parse individual cells from scATAC-seq data.')
    parser.add_option('-m',
                      dest="min",
                      help='Minimum number of reads',
                      type="int"
    )

    parser.add_option('-o',
                      dest="output",
                      help='Output BAM file name',
    )

    if len(sys.argv) < 4:
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

    os.chdir('output')
    input_BAM = list()
    for file in os.listdir():
        if file.endswith('.sam'):
            barID = file.split(".")[0]
            pysam.fixmate("-m", file, barID + "_fixmate.bam")
            pysam.sort("-o", barID + "_sort.bam", barID + "_fixmate.bam")
            pysam.markdup("-r", barID + "_sort.bam", barID + ".bam")
            os.remove(file)
            os.remove(barID + "_fixmate.bam")
            os.remove(barID + "_sort.bam")
            input_BAM.append(barID + ".bam")

    merge_parameters = ['-f',args.output] + input_BAM
    pysam.merge(*merge_parameters)

if __name__ == '__main__':
    main()
