import gzip
import xml.etree.ElementTree as ET
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


def get_motif_alts(meme_xml: str):
    tree = ET.parse(meme_xml)
    return [motif.get('alt') for motif in tree.findall('./motifs/')]


def fimo_txt_to_bed(fimo_txt: str, motif_alts: list, out_dir: str = '.'):
    output_files = [open('{}/MOTIF{}.bed'.format(out_dir, i + 1), 'wt') for i, motif in enumerate(motif_alts)]
    motif_alt_map = {motif: i for i, motif in enumerate(motif_alts)}
    with openfile(fimo_txt, 'rt') as f:
        for line in f:
            if not line.strip() or line.startswith('#'):
                continue
            header = line.strip().split('\t')
            break
        for line in f:
            if not line.strip() or line.startswith('#'):
                continue
            fields = dict(zip(header, line.strip().split('\t')))
            i = motif_alt_map[fields['motif_alt_id']]
            output_files[i].write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                fields['sequence_name'],
                int(fields['start']) - 1,
                fields['stop'],
                fields['motif_alt_id'],
                fields['score'],
                fields['strand']
            ))
    for f in output_files:
        f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fimo_txt', help='Name of the .txt file which is output of Fimo')
    parser.add_argument('meme_xml', help='MEME XML file')
    parser.add_argument('--out-dir', dest='out_dir', help='Output directory', default='.')
    args = parser.parse_args()
    motif_alts = get_motif_alts(args.meme_xml)
    fimo_txt_to_bed(args.fimo_txt, motif_alts, args.out_dir)
