'''
Created on Nov 7, 2013

@author: jason & kostas
'''
import unittest
from org.umd.assemblytest.readcoverage.coverage import parse_fasta_file, ContigBPCoverage, ContigWindowCoverage
from org.umd.assemblytest.readcoverage.samfile import SamFile

# It's not very straightforward to
# implement unit cases for full coverage tests.
class ContigCovTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

    def lengthsOfMaps(self):
        cl = parse_fasta_file('../../../../../data/influenza-A/influenza-A.assembly.fasta')
        samfile = SamFile.read('../../../../../tutorial/read_coverage/influenza-A.sam')
        bp_cov = ContigBPCoverage(samfile, cl)
        w_cov = ContigWindowCoverage(bp_cov, 100, 100)
        self.assertEquals(len(w_cov.contig_coverage), len(w_cov.contig_window_starting_points))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
