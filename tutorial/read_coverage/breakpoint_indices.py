"""
Input: an assembly fasta file and a set of unaligned reads in fasta format.
Input: alpha, window size at the beginning of the unaligned reads.
Output: a distribution over the indices of the assembly where errors are likely
"""

import sys
from optparse import OptionParser






def Main():
	parser = OptionParser()
	parser.add_option("-a","--assembly-file", dest = "assembly_file")
	parser.add_option("-u","--unaligned-file",dest = "unaligned_file")
	parser.add_option("--alpha",dest = "alpha")

	(options, args) = parser.parse_args()

	if not options.assembly_file:
		print 'Provide assembly file (-a, --assembly-file)'
		sys.exit()

	if not options.unaligned_file:
		print 'Provide unaligned reads file (-u, --unaligned-file)'
		sys.exit()

	if not options.alpha:
		print 'Provide alpha (--alpha)'
		sys.exit()

if __name__=="__main__":
	Main()