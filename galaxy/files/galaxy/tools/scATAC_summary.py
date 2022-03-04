#!/usr/bin/env python

import sys
import optparse
import gzip
import pysam
from functools import reduce

def main():
    """ main function """
    parser = optparse.OptionParser(usage='%prog [-h] [-a Raw Reads] [-b Unique BAM] [-c Barcode-corrected BAM] [-d PCR duplicated BAM] [-e Final BAM]',
                                   description='Generate scATAC-seq summary statistics.')
    parser.add_option('-a',
        dest="raw_reads",
        help='Raw FASTQ file',
    )
    parser.add_option('-b',
        dest="uniq_bam",
        help='Uniquely-mapped BAM file'
    )
    parser.add_option('-c',
        dest="barcode_bam",
        help='Barcode-corrected BAM file'
    )
    parser.add_option('-d',
        dest="pcr_bam",
        help='PCR de-duplicated BAM file'
    )
    parser.add_option('-e',
        dest="final_bam",
        help='Final processed BAM file'
    )

    if len(sys.argv) < 10:
        parser.print_help()
        exit('error: too few arguments')

    args = parser.parse_args()[0]
    raw_reads = args.raw_reads
    uniq_bam = args.uniq_bam
    barcode_bam = args.barcode_bam
    pcr_bam = args.pcr_bam
    final_bam = args.final_bam

    print("================================ Summary ==================================")
    file = gzip.open(raw_reads, 'rt')
    lineCount = 0
    while True:
        line = file.readline()
        line = file.readline()
        line = file.readline()
        line = file.readline()
        if line == "": break
        lineCount = lineCount + 1
    file.close()
    print("Total number of raw reads: "+str(lineCount))

    readCount = pysam.AlignmentFile(uniq_bam, "rb").mapped
    print("Uniquely mapped reads (MAPQ>=30): " + str(readCount))

    readCount_BAR = pysam.AlignmentFile(barcode_bam, "rb").mapped
    print("Reads left after barcode correction: " + str(readCount_BAR))

    print("Unique barcode combinations: ")

    readCount_PCR = pysam.AlignmentFile(pcr_bam, "rb").mapped
    dupRate = round(((readCount_BAR - readCount_PCR) / readCount_BAR) * 100,2)
    print("Estimated PCR duplication rate: " + str(dupRate))

    readCount = pysam.AlignmentFile(final_bam, "rb").mapped
    print("Total number of reads left: " + str(readCount))

    #print("Number of cells with more than " + str(args.min_reads) + " reads: ")


if __name__ == '__main__':
    main()
