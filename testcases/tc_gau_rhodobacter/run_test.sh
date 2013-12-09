#!/usr/bin/sh

python ../../src/matePairAnalysis.py --fasta ../../data/rhodobacter/rhodobacterMod.assembly.fasta -1 ../../data/rhodobacter/rhodobacter.sequences.1.fasta -2 ../../data/rhodobacter/rhodobacter.sequences.2.fasta --gau
rm *.sam *.bam *.bai
#python eval_gau_del.py

exit $?