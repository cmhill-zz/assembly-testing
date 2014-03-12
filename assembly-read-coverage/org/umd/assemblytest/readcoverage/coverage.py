'''
Created on Nov 7, 2013

@author: jason & kostas
'''

import numpy as np

'''
Read a FASTA assembly file and store the {contig_id, contig_length}
pairs in a dictionary.
'''

def parse_fasta_file(filename):
    contig_length = dict()
    try:
        with open(filename) as f:
            current_key = None
            for line in f:
                line = line.strip();
                if line[0] == '>':
                    current_key = line[1:]  # update current key
                    contig_length[current_key] = 0
                else:
                    contig_length[current_key] += (len(line))
    except EnvironmentError as err:
        print "Unable to open FASTA file: {}".format(err);
    return contig_length

class ContigBPCoverage:

    def __init__(self, samfile, contig_length):
        self.contig_length = contig_length
        self.contig_coverage = dict()
        for contig_id in contig_length:
            cov = np.array([len(samfile.coverage(contig_id, pos, 1)) for pos in range(1, contig_length[contig_id] + 1)], dtype=np.float32)
            self.contig_coverage[contig_id] = cov

class ContigWindowCoverage(object):

    '''
    Computes the coverage of a contig given a
    specified window size and sliding step for the window.
    Note that binning is a special case of sliding windows when the step size
    just happens to be equal to window length.
    '''

    '''
    Constructor
    @param samfile a Samfile object
    @param contig_data a ContigData object
    @param window_length a positive integer representing the window length
    @param step_size a positive integer representing the step size for the window.
    '''
    def __init__(self, bp_coverage, window_length, step_size):
        # Sanity checking
        if window_length < 0 or step_size < 0:
            raise RuntimeError, "ContigCoverage constructor: Provided negative argument."
        if bp_coverage is None:
            raise RuntimeError, "ContigCoverage constructor: Provided None argument."
        # Main algorithm
        self.window_length = window_length
        self.step_size = step_size
        self.contig_length = bp_coverage.contig_length
        self.contig_coverage = {}  # associates contigs with their windows' coverages
        self.contig_window_start_index = {}
        window = np.ones(window_length) / window_length
        for contig_id in bp_coverage.contig_length:
            if window_length == 1:
                cov = bp_coverage.contig_coverage[contig_id]
            else:
                cov = np.convolve(bp_coverage.contig_coverage[contig_id], window, 'valid')
            starting_points = range(len(cov))
            if step_size > 1:
                cov = cov[0::step_size]
                starting_points = starting_points[0::step_size]
            self.contig_coverage[contig_id] = cov
            self.contig_window_start_index[contig_id] = starting_points
