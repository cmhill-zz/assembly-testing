#! /usr/bin/bash

# First build the index that bowtie2 will use the align the reads.
bowtie2-build ../../data/rhodobacter/rhodobacter.assembly.fasta rhodobacter.bt2

# Run bowtie2 to get the mate pair alignments.  400 and 600 are the upper and lower bounds to search for a proper mate pair alignment.
bowtie2 -x rhodobacter.bt2 -f -1 ../../data/rhodobacter/rhodobacter.sequences.1.fasta -2 ../../data/rhodobacter/rhodobacter.sequences.2.fasta -I 400 -X 600 -S rhodobacter.sequences.sam

# Quick command to build a histogram of the insert sizes.
awk '{if (int($9) > 0) print $9}' rhodobacter.sequences.sam | sort -nr | uniq -c > rhodobacter.sequences.insert_sizes