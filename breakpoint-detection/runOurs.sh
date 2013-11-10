#!/bin/bash

if [ "$1" != "" ]; then
    ALPHA=$1
else
    ALPHA=5
fi

python breakpoint_indices.py -a ../data/influenza-A/influenza-A.assembly.fasta -u unaligned.txt --alpha $ALPHA
