#!/usr/bin/sh

python ../../../src/matePairAnalysis.py --ce --ce_threshold 3.5 --fasta rhodobacter.assembly.fasta -1 rhodobacter.sequences.1.fasta -2 rhodobacter.sequences.2.fasta > match.txt
rm *.sam *.bam *.bai &> /dev/null
python eval_rhodobacter_all.py

exit $?