#!/bin/bash

# First build the index that bowtie2 will use the align the reads.
bowtie2-build ../../data/influenza-A/influenza-A.assembly.fasta influenza-A.bt2

# Run bowtie2 to get the alignments.
bowtie2 -x influenza-A.bt2 -f -U ../../data/influenza-A/influenza-A.sequences.fasta -S influenza-A.sam

# Quick and dirty command to get the starting point and binning it in 100bp segments.
awk '{print int($4/100)}' influenza-A.sam | sort -nr | uniq -c > influenza-A.cov