"""
converts a FASTQ file to a FASTA file
"""

import sys
import subprocess

if len(sys.argv) < 3:
	print 'provide an input and output file'
	sys.exit()

infile = sys.argv[1]
outfile = sys.argv[2]

execString = "awk 'NR % 4 == 1 || NR % 4 == 2' "+infile+" | sed -e 's/@/>/' > "+outfile

print execString

subprocess.call(execString,shell=True)