'''
Created on Nov 11, 2013

@author: kzampog
'''

import argparse, sys, os
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description='Compares detected misassemblies against given oracle (ground truth)')
    parser.add_argument('-m', '--misassemblies', required=True, help='Misassemblies file in FASTA-like format', metavar='MISASSEMBLIES_FILE', dest='misassemblies_file')
    parser.add_argument('-o', '--oracle', required=True, help='Oracle file in FASTA-like format', metavar='ORACLE_FILE', dest='oracle_file')
    args = parser.parse_args()
    if not os.path.exists(args.misassemblies_file):
        print 'Misassemblies file not found'
        sys.exit(1)
    if not os.path.exists(args.oracle_file):
        print 'Oracle file not found'
        sys.exit(1)
    return args

def parse_fasta_file(filename):
    str_dict = {}
    try:
        with open(filename) as f:
            current_key = None
            for line in f:
                line = line.strip();
                if line[0] == '>':
                    current_key = line[1:]  # update current key
                    str_dict[current_key] = ''
                else:
                    str_dict[current_key] += line
    except EnvironmentError as err:
        print "Unable to open FASTA file: {}".format(err);
    return str_dict

def concatenate_consistently(dict1, dict2):
    bv1 = ''
    bv2 = ''
    for cid in dict1:
        bv1 += dict1[cid]
        bv2 += dict2[cid]
    bv1 = np.array([int(i) for i in bv1], dtype=np.bool)
    bv2 = np.array([int(i) for i in bv2], dtype=np.bool)
    return bv1, bv2

def jaccard_index(bv1, bv2):
    den = np.count_nonzero(bv1 | bv2)
    if den == 0:
        return 1
    else:
        return (1.0 * np.count_nonzero(bv1 & bv2)) / den

def f_score(bv1, bv2):
    den = np.count_nonzero(bv1) + np.count_nonzero(bv2)
    if den == 0:
        return 1
    else:
        return (2.0 * np.count_nonzero(bv1 & bv2)) / den

if __name__ == '__main__':
    args = parse_args()
    misassemblies_dict = parse_fasta_file(args.misassemblies_file)  # returns a dictionary which maps contig ids to the contig itself
    # print misassemblies_dict
    oracle_dict = parse_fasta_file(args.oracle_file)  # same thing
    misassemblies_bv, oracle_bv = concatenate_consistently(misassemblies_dict, oracle_dict)  # Returns two boolean vectors
    ji = jaccard_index(misassemblies_bv, oracle_bv)  # Calculates the jaccard index for the two vectors
    fs = f_score(misassemblies_bv, oracle_bv)  # Same for the f-score
    print "Comparison with ground truth oracle..."
    print 'Jaccard index: {0}'.format(ji)
    print 'F-score: {0}'.format(fs)
    if fs < 0.5:  # Tune-able parameter
        print 'Test FAILED'
        sys.exit(1)
    else:
        print 'Test SUCCESSFUL'
