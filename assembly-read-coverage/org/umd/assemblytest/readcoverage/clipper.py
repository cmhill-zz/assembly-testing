'''
Created on Nov 10, 2013

@author: kzampog
'''

import argparse, sys, os, subprocess
from samfile import SamFile
import coverage as cov
import statistics as stat
import graphics as gr

def parse_args():
    parser = argparse.ArgumentParser(description='Detects assembly regions of extreme coverage')
    parser.add_argument('-a', '--assembly', required=True, help='Assembly file in FASTA format', metavar='ASSEMBLY_FASTA', dest='assembly_file')
    parser.add_argument('-r', '--reads', required=True, help='Read sequences file in FASTA format', metavar='READS_FASTA', dest='reads_file')
    parser.add_argument('-w', '--window_length', default=1, type=int, help='Sliding window length (integer)', metavar='WIN_LEN')
    parser.add_argument('-s', '--window_slide_step', default=1, type=int, help='Window sliding step (integer)', metavar='WIN_STEP')
    parser.add_argument('-t', '--test_type', required=True, help='Statistical test type used to determine extreme coverage; can be either Gaussian or Percentile', metavar='TEST_TYPE')
    parser.add_argument('-p', '--test_param', type=float, required=True, help='Statistical test parameter (float)', metavar='TEST_PARAM')
    parser.add_argument('-o', '--output_dir', default='./out/', required=False, help='Output file directory', metavar='OUT_DIR')
    args = parser.parse_args()
    # File and path existence checks
    if not os.path.exists(args.assembly_file):
        print 'Could not open assembly file.'
        sys.exit(1)
    if not os.path.exists(args.reads_file):
        print 'Could not open read sequences file.'
        sys.exit(1)
    if not os.path.isdir(args.output_dir):
        try:
            os.makedirs(args.output_dir)
        except OSError as err:
            print 'Could not create output directory: {}'.format(err);
    if len(args.output_dir) > 0 and args.output_dir[-1] != '/':
        args.output_dir += '/'
    base_name = os.path.basename(args.assembly_file)[::-1]
    base_name = os.path.splitext(base_name)[-1][::-1][0:-1]
    args.base_name = base_name
    return args

def generate_sam_file(args):
    samname = args.output_dir + args.base_name + '.sam'
    bt2name = args.output_dir + args.base_name + '.bt2'
    stdout_file = open(bt2name + '.stdout', 'w')
    stderr_file = open(bt2name + '.stderr', 'w')
    command1 = 'bowtie2-build ' + args.assembly_file + ' ' + bt2name
    retval = subprocess.call(command1, stdout=stdout_file, stderr=stderr_file, shell=True)
    stdout_file.close()
    stderr_file.close()
    if retval != 0:
        print 'BowTie2 indexing failed'
        sys.exit(1)
    stdout_file = open(samname + '.stdout', 'w')
    stderr_file = open(samname + '.stderr', 'w')
    # bowtie2-align same as bowtie2 (script)?
    command2 = 'bowtie2-align -x ' + bt2name + ' -f -U ' + args.reads_file + ' -S ' + samname
    retval = subprocess.call(command2, stdout=stdout_file, stderr=stderr_file, shell=True)
    if retval != 0:
        print 'BowTie2 alignment failed'
        sys.exit(1)
    return samname


if __name__ == '__main__':
    args = parse_args()
    cov_params_str = '.W{0}_S{1}'.format(args.window_length, args.window_slide_step)
    test_params_str = '_{0}_P{1}'.format(args.test_type, args.test_param)
    partial_name = args.output_dir + args.base_name + cov_params_str + test_params_str
    print 'Calculating alignments (SAM file) using BowTie2...'
    sam_filename = generate_sam_file(args)
    print 'Parsing SAM file...'
    samfile = SamFile.read(sam_filename)
    print 'Reading auxiliary data from assembly FASTA file...'
    cdata = cov.parse_fasta_file(args.assembly_file)
    print 'Calculating base-pair level coverage...'
    bp_cov = cov.ContigBPCoverage(samfile, cdata)
    print 'Calculating window-averaged coverage...'
    w_cov = cov.ContigWindowCoverage(bp_cov, args.window_length, args.window_slide_step)
    print 'Performing statistical test...'
    st = stat.CoverageStatistics(w_cov, args.test_type, args.test_param)
    print 'Results:'
    print st.to_string()
    print 'Writing test results to text files...'
    st.write_all_files(partial_name)
    print 'Writing test results to image files...'
    gr.write_all_images(bp_cov, w_cov, st, 20, 10, partial_name)
    print 'Done'  # THIS LINE IS DEDICATED TO JASON
