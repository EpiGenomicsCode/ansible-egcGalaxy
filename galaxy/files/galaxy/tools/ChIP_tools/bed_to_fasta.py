import gzip
from twobitreader import TwoBitFile
import argparse


def is_gz_file(filepath):
    """
    Check first byte of file to see if it is gzipped
    """
    with open(filepath, 'rb') as test_f:
        return test_f.read(2) == b'\x1f\x8b'


def openfile(filepath, mode='r'):
    if is_gz_file(filepath):
        return gzip.open(filepath, mode)
    return open(filepath, mode)


def compl(seq, rev=True):
    """
    Return the complement of a sequence.
    """
    comp = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N',
            'a': 't', 't': 'a', 'g': 'c', 'c': 'g', 'n': 'n'}
    return ''.join(map(comp.__getitem__, seq if not rev else reversed(seq)))


def bed_to_fasta(bed_fn: str, twobit_fn: str, out_fn: str):
    tb = TwoBitFile(twobit_fn)
    with openfile(bed_fn, 'rt') as f, open(out_fn, 'wt') as out:
        for line in f:
            if not line.strip() or line.startswith('#'):
                continue
            chrom, start, end, name, score, strand = line.strip().split('\t')
            seq = tb[chrom][int(start):int(end)] if strand == '+' else compl(tb[chrom][int(start):int(end)])
            out.write('>{}:{}-{}({})\n{}\n'.format(chrom, start, end, strand, seq))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bed', help='BED file')
    parser.add_argument('twobit', help='2bit file')
    parser.add_argument('out', help='Output file')
    args = parser.parse_args()

    bed_to_fasta(args.bed, args.twobit, args.out)
