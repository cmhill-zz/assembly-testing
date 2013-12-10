#!/usr/bin/sh

python ../../../src/matePairAnalysis.py --gau --fasta insDelTest.fasta -1 r1.fq -2 r2.fq > match.txt
rm *.sam *.bam *.bai &> /dev/null
python eval_gau_ins_del.py

exit $?