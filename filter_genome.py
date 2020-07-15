import os,re
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-genome', required=True, dest='genome', help='Input genome fasta')
parser.add_argument('-gff', required=True, dest='gff', help='Input gff3 file')
parser.add_argument('-fa', required=True, dest='fa', help='Output filter fasta file')
parser.add_argument('-fgff', required=True, dest='fgff', help='Output filter gff file')
parser.add_argument('-cut', default='5000', dest='cut', type=int, help='Min contig length for filter')
options = parser.parse_args()

if not os.path.exists(options.genome) or not os.path.exists(options.gff):
    print("Input file is not exists")
    sys.exit()

out_fa = open(options.fa, 'w')
flag = 0
del_contig = {}
with open(options.genome,'r') as raw:
    for line in raw:
        if line.startswith('>'):
            col = line.strip().split()
            contig_len = int(col[-1].split('=')[-1])
            contig_id  = re.sub('^>','',col[0])
            if contig_len < options.cut:
                del_contig[contig_id] = 1
                flag = 0
            else:
                out_fa.write(line)
                flag = 1
        else:
            if flag == 1:
                out_fa.write(line)
out_fa.close()

out_gff = open(options.fgff, 'w')
with open(options.gff, 'r') as rawgff:
    for line in rawgff:
        contig_id = line.strip().split('\t')[0]
        if contig_id in del_contig:
            continue
        else:
            out_gff.write(line)
out_gff.close()
