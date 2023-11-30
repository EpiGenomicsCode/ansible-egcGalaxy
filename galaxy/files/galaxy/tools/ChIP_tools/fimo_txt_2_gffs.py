import csv
import argparse
import time


class Gff_File_Row:
    def __init__ (self):
        self.id_chr = None
        self.first_bp = None
        self.last_bp = None
        self.subtype = None
        self.score = None
        self.strand_dir = None
        #self.sequence = None  


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input' , dest='fimo_txt', required=True, help='Name of the .txt file which is output of Fimo')
    args = parser.parse_args()
    #time.sleep(60)
    print (" Conversion started ..." )
    parsed_fimo_txt = Parse_Fimo_Txt(args.fimo_txt)
    print ("fimo txt file parsed" )
    gff_file          = Extract_Gff_File_Info(parsed_fimo_txt)
    print ("gff file data extracted" )
    gff_files         = Split_Gff_File(gff_file)
    print ("gff file splitted" )
    #Write_Bed_Files(bed_files)
    Write_Gff_Files(gff_files)
    print ("gff file written in the output file" )

def Parse_Fimo_Txt(file_name):
    with open(file_name) as data:
        data_reader = csv.reader(data, delimiter='\t')
        raw_data = list (data_reader)
    return raw_data


def Extract_Gff_File_Info (parsed_fimo_txt):
    gff_file = []
    for line in parsed_fimo_txt:
        int_count = 0
        ## a proper gff line should have at least two integers a start and a stop sequence, otherwise it is a header or a comment line.
        for element in line:
            try:
                _ = int(str(element))
                int_count += 1
            except:
                pass
        if (int_count > 1 ): 
            # it is a gff line
            gff_file_row = Gff_File_Row()
            gff_file_row.id_chr     =     (str(line[2]))
            gff_file_row.first_bp   = int((str(line[3])))
            gff_file_row.last_bp    = int((str(line[4])))
            gff_file_row.score      = float(   line[6])
            gff_file_row.strand_dir =     (str(line[5]))
            gff_file_row.subtype    = int((str(line[0])))
            gff_file.append (gff_file_row)
        else:
            print ("skipped line is %s" % str(line))
    return (gff_file)


def Split_Gff_File (gff_file):
    max_subtypes = 0
    for gff_file_row in gff_file:
        if (gff_file_row.subtype > max_subtypes):
            max_subtypes = gff_file_row.subtype
    print ("max_subtype is:")
    print (max_subtypes)
    gff_files = [[] for i in range (max_subtypes)]
    for gff_file_row in gff_file:
        gff_files[gff_file_row.subtype - 1].append (gff_file_row)
    return (gff_files)


def Write_Bed_Files(bed_files):

    file_name = 'motif' + '1' + '.bed'
    fileM = open(file_name,'w')
    for i in range (len(bed_files)):
        file_name = 'motif' + str(i+1) + '.bed'
        fileM = open(file_name,'w')
        #fileM.write ('Chrom, Start, End, Name, Score, Strand \n')
        for bed_file_row in bed_files[i]:
            fileM.write(bed_file_row.id_chr + '\t')
            fileM.write(str(bed_file_row.first_bp)+ '\t')
            fileM.write(str(bed_file_row.last_bp)+ '\t')
            fileM.write('motif' + str (bed_file_row.subtype)+ '\t')
            fileM.write(str(bed_file_row.score)+ '\t')
            fileM.write(bed_file_row.strand_dir)
            fileM.write('\n')


def Write_Gff_Files(gff_files):
    file_name = 'motif' + '1' + '.gff'
    fileM = open(file_name,'w')
    for i in range (len(gff_files)):
        file_name = 'MOTIF' + str(i + 1) + '.gff'
        fileM = open(file_name,'w')
        #fileM.write ('Chrom, Start, End, Name, Score, Strand \n')
        #fileM.write ('##gff-version 3 \n')
        for gff_file_row in gff_files[i]:
            fileM.write(gff_file_row.id_chr + '\t')
            fileM.write("fimo" + '\t')   # for gff
            fileM.write('motif' + str (gff_file_row.subtype)+ '\t')
            fileM.write(str(gff_file_row.first_bp)+ '\t')
            fileM.write(str(gff_file_row.last_bp)+ '\t')
            fileM.write(str(gff_file_row.score)+ '\t')  # for gff
            fileM.write(gff_file_row.strand_dir+ '\t' )
            fileM.write('.'+ '\t')
            fileM.write('motif' + str (gff_file_row.subtype)+ ';')
            fileM.write('\n')

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == "__main__":
    main()
