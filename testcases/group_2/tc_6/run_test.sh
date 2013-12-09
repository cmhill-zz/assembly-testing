#!/usr/bin/sh

python ../../../src/matePairAnalysis.py --fasta rhodobacterMod.assembly.fasta -1 rhodobacter.sequences.1.fasta -2 rhodobacter.sequences.2.fasta --gau > match.txt
rm *.sam *.bam *.bai &> /dev/null
#python eval_gau_del.py

exit $?