#!/usr/bin/env python

import sys
import optparse
import gzip
import pysam
from functools import reduce

def main():
    """ main function """
    parser = optparse.OptionParser(usage='%prog [-h] [-a Raw Reads] [-b Unique reads]',
                                   description='Generate scATAC-seq summary statistics.')
    parser.add_option('-a',
        dest="raw_reads",
        help='Raw FASTQ file',
    )
    parser.add_option('-b',
        dest="uniq_reads",
        help='Unique BAM file'
    )

    if len(sys.argv) < 4:
        parser.print_help()
        exit('error: too few arguments')

    args = parser.parse_args()[0]
    raw_reads = args.raw_reads
    uniq_reads = args.uniq_reads

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

    #samfile = pysam.AlignmentFile(uniq_reads, "rb")
    cmd = "samtools idxstats %bamfile | awk -F '\t' '{s+=$3+$4}END{print s}'" % uniq_reads
    readCount = float(subprocess.check_output(shlex.split(cmd)))
    #print(pysam.idxstats(uniq_reads))
    #readCount = reduce(lambda x, y: x + y, [ int(l.rstrip('\n').split('\t')[2]) for l in pysam.idxstats(uniq_reads) ])
    print("Uniquely mapped reads (MAPQ>=30): " + str(readCount))


if __name__ == '__main__':
    main()
