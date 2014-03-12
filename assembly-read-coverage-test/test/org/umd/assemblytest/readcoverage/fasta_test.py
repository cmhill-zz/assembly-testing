'''
Created on Nov 7, 2013

@author: jason & kostas
'''
import unittest
from org.umd.assemblytest.readcoverage.coverage import parse_fasta_file;

class FastaTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

    def testParsing(self):
        cl = parse_fasta_file('resources/dummy_fasta.txt');
        self.assertTrue('1' in cl)
        self.assertTrue('2' in cl)
        self.assertTrue('non_numerical_id' in cl)
        self.assertTrue('10' in cl)

        self.assertEquals(cl['1'], 5)
        self.assertEquals(cl['2'], 20)
        self.assertEquals(cl['non_numerical_id'], 0)
        self.assertEquals(cl['10'], 10)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
