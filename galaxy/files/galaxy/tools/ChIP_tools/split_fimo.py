import argparse

# motif_id  motif_alt_id    sequence_name   start   stop    strand  score   p-value q-value matched_sequence
# GGTGDRTGGGTSTGKTDTST  MEME-3  chrIV   25  44  -   32.2584 1.04e-11    0   GGTGTGTGGGTGTGGTGTGT
# GGTGDRTGGGTSTGKTDTST  MEME-3  chrXI   28  47  -   32.2584 1.04e-11    0   GGTGTGTGGGTGTGGTGTGT
# GGTGDRTGGGTSTGKTDTST  MEME-3  chrXI   28  47  -   32.2584 1.04e-11    0   GGTGTGTGGGTGTGGTGTGT
# GGTGDRTGGGTSTGKTDTST  MEME-3  chrX    29  48  -   32.2584 1.04e-11    0   GGTGTGTGGGTGTGGTGTGT

def process_data(input_data, out_dir):
    # Split the data by lines and remove the header
    lines = input_data.strip().split('\n')[1:]

    # Create a dictionary to store data based on motif_alt_id
    data_dict = {}
    for line in lines:
        # Ignore lines starting with #
        if not line.startswith('#'):
            # Split each line by tabs
            parts = line.split('\t')
            # Check if the line contains the expected number of elements
            if len(parts) >= 5:  # Check for at least 5 elements in the line

                # Extract relevant information
                motif_alt_id = parts[1]
                motif_alt_id_number = ''.join(filter(str.isdigit, motif_alt_id))
                start = parts[3]
                stop = parts[4]
                sequence = '\t'.join(parts[2:])

                # Check for duplicates based on start and stop
                if (start, stop) not in data_dict.get(motif_alt_id, []):
                    if motif_alt_id not in data_dict:
                        data_dict[motif_alt_id] = set()
                    data_dict[motif_alt_id].add((start, stop))
                    # Write data to files
                    with open('{}/MOTIF{}.gff'.format(out_dir, motif_alt_id_number), "a") as file:
                        file.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                            parts[2],
                            'fimo',
                            parts[1],
                            parts[3],
                            parts[4],
                            parts[6],
                            parts[5],
                            '.',
                            parts[1]
                        ))
            else:
                print(f"Skipping malformed line: {line}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fimo_txt', help='Name of the .txt file which is output of Fimo')
    parser.add_argument('--out-dir', dest='out_dir', help='Output directory', default='.')
    args = parser.parse_args()

    # Read data from the input file
    with open(args.fimo_txt, 'r') as file:
        data = file.read()
    process_data(data, args.out_dir)
