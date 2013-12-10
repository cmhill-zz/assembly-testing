#!/bin/bash

# First build the index that bowtie2 will use the align the reads.
bowtie2-build ../data/influenza-A/influenza-A.assembly.fasta influenza-A.bt2

# Run bowtie2 to get the alignments.
bowtie2 --un unaligned.txt -x influenza-A.bt2 -f -U ../data/influenza-A/influenza-A.sequences.fasta -S influenza-A.sam

rm -f inf*