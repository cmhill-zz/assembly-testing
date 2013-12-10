#!/bin/bash

echo $1

python breakpoint_indices.py -a ../../data/influenza-A/influenza-A.assembly.fasta -u unaligned.txt --alpha "$1"