"""
Generates a file from an assembly file which is the unaligned reads from bowtie2.
"""

import sys
import subprocess

if (len(sys.argv) < 4):
	print 'Provide an input assembly file, a reads file, and an output file.'
	sys.exit()

assembly_file = sys.argv[1]
reads_file = sys.argv[2]
output_file = sys.argv[3]

# First build the index that bowtie2 will use the align the reads.
execString = "bowtie2-build <ASSEMBLY_FILE> assemblyIndex.bt2"
execString = execString.replace("<ASSEMBLY_FILE>",assembly_file)

subprocess.call(execString,shell=True)

# Run bowtie2 to get the alignments.
execString = "bowtie2 --un <OUTPUT_FILE> -x assemblyIndex.bt2 -f -U <READS_FILE> -S output.sam"
execString = execString.replace("<READS_FILE>",reads_file)
execString = execString.replace("<OUTPUT_FILE>",output_file)

subprocess.call(execString,shell=True)

execString = "rm -f *assemblyIndex*"
subprocess.call(execString,shell=True)