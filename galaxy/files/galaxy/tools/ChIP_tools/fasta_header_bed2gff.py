import argparse

class Fasta_Line_Elements:
    def __init__ (self, header_type):
        self.chr = None 
        self.start  = None 
        self.end = None 
        self.strand = None  
        self.seq = None 
        self.header_type = header_type


def read_file_lines(file_name):
    list_lines =  open(file_name).readlines()
    return list_lines


def Extract_fasta_lines_elements(fasta_lines, header_format):
    fasta_lines_elements = []

    fasta_line_elements = Fasta_Line_Elements(header_format)
    header_line_detected = False
    sequence_line_detected = False
    for line in fasta_lines:
        if (line[0] == ">"):
            header_line_detected = True
            # there is space chracter at the end of the line
            fasta_line_elements.chr = line.split(':')[0][1:]
            tmp_string_coord = line.split(':')[1][:-4]
            fasta_line_elements.start = tmp_string_coord.split('-')[0]
            fasta_line_elements.end = tmp_string_coord.split('-')[1]
            fasta_line_elements.strand = line [-3]

        else:
            sequence_line_detected = True
            fasta_line_elements.seq = line
            print (fasta_line_elements.seq)
         
        if (header_line_detected and sequence_line_detected):
            fasta_lines_elements.append(fasta_line_elements)
            fasta_line_elements = Fasta_Line_Elements(header_format)
            header_line_detected = False
            sequence_line_detected = False
   
    return (fasta_lines_elements)

def Write_fasta_file_with_gff_header_format(fasta_lines_elements):

  file_name = 'fasta_file_gff_format_header.fasta'
  fileM = open(file_name,'w')
  for fasta_line_elements in fasta_lines_elements:
      fileM.write(">" + fasta_line_elements.chr + ':' 
      + str(int(fasta_line_elements.start) + 1) + '-'  
      + fasta_line_elements.end                 + '(' 
      + fasta_line_elements.strand              + ')\n')


      fileM.write(fasta_line_elements.seq)

    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input' , dest='fasta_file', required=True, help='Name of the fasta file')
    parser.add_argument('--header_format' , dest='header_format', required=True, help='is the header of fasta lines in gff or bed format')
    args = parser.parse_args()
    print (" process started ..." )
    fasta_lines = read_file_lines(args.fasta_file)
    print ("fasta lines read" )
    fasta_lines_elements = Extract_fasta_lines_elements(fasta_lines, args.header_format)
    print ("elements in fasta line (chr, start coordinate, stop coordinate, strand, sequence) extracted" )
    if (args.header_format == 'bed'):
        Write_fasta_file_with_gff_header_format(fasta_lines_elements)
        print ('finished writing fasta file with headers in gff format')
    else:
        print ('Nothing is done!. Your header_format given as input is not bed. This code only converts fasta file with headers from bed format to gff format')



if __name__ == "__main__":
    main()
