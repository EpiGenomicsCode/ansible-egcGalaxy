#!/usr/bin/env python

import sys
import optparse
import gzip
import pysam
import statistics

def main():
    """ main function """
    parser = optparse.OptionParser(usage='%prog [-h] [-a Raw Reads] [-b Unique BAM] [-c Barcode-corrected BAM] [-d Unique Barcodes][-e PCR duplicated BAM] [-f Final BAM] [-g Minimum read threshold] [-i Final Barcode count]',
                                   description='Generate scATAC-seq summary statistics.')
    parser.add_option('-a',
        dest="fastqc_raw",
        help='FASTQC raw file',
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
        dest="uniq_bar",
        help='List of unique barcodes'
    )
    parser.add_option('-e',
        dest="pcr_bam",
        help='PCR de-duplicated BAM file'
    )
    parser.add_option('-f',
        dest="final_bam",
        help='Final processed BAM file'
    )
    parser.add_option('-g',
        dest="min_reads",
        help='Minimum read threshold'
    )
    parser.add_option('-i',
        dest="final_barcode",
        help='Final barcode utilization statistics file'
    )

    if len(sys.argv) < 16:
        parser.print_help()
        exit('error: too few arguments')

    args = parser.parse_args()[0]
    raw_reads = args.fastqc_raw
    uniq_bam = args.uniq_bam
    barcode_bam = args.barcode_bam
    uniq_bar = args.uniq_bar
    pcr_bam = args.pcr_bam
    final_bam = args.final_bam
    min_reads = int(args.min_reads)
    final_barcode = args.final_barcode

    print("================================ Summary ==================================")
    readCount_RAW = 0
    with open(raw_reads) as fb:
        for i, line in enumerate(fb):
            if line.startswith('Total Sequences'):
                readCount_RAW = int(line.split()[2])
    print("Total number of raw reads: "+str(readCount_RAW))

    readCount = pysam.AlignmentFile(uniq_bam, "rb").mapped
    print("Uniquely mapped reads (MAPQ>=30): " + str(readCount))

    readCount_BAR = pysam.AlignmentFile(barcode_bam, "rb").mapped
    print("Reads left after barcode correction: " + str(readCount_BAR))

    with open(uniq_bar) as fb:
        for barcount, line in enumerate(fb):
            pass
    barcount = barcount + 1
    print("Unique barcode combinations detected: " + str(barcount))

    readCount_PCR = pysam.AlignmentFile(pcr_bam, "rb").mapped
    dupRate = round(((readCount_BAR - readCount_PCR) / readCount_BAR) * 100,2)
    print("Estimated PCR duplication rate: " + str(dupRate))

    readCount = pysam.AlignmentFile(final_bam, "rb").mapped
    print("Total number of reads left: " + str(readCount))

    readStats = []
    with open(final_barcode) as fb:
        for count, line in enumerate(fb):
            if int(line.split()[1]) > min_reads:
                readStats.append(int(line.split()[1]))
    print("Number of cells with more than "+ str(min_reads) + " reads: " + str(len(readStats)))
    print("Min number of reads for selected cells: " + str(min(readStats)))
    print("Median number of reads for selected cells: " + str(statistics.median(readStats)))
    print("Max number of reads for selected cells: "+ str(max(readStats)))

if __name__ == '__main__':
    main()
