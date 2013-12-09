#!/usr/bin/sh

python ../../src/matePairAnalysis.py --fasta delTest.fasta -1 r1.fq -2 r2.fq --gau > match.txt
rm *.sam *.bam *.bai &> /dev/null
python eval_gau_del.py

exit $?