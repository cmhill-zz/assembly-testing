#!/usr/bin/sh

python ../../src/matePairAnalysis.py --fasta insDelTest.fasta -1 r1.fq -2 r2.fq --gau
rm *.sam *.bam *.bai
python eval_gau_ins_del.py

exit $?