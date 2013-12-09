#!/bin/bash

python ../../../src/matePairAnalysis.py --ce --fasta insTest.fasta -1 r1.fq -2 r2.fq --ce_threshold 2.5 --ce_windowsize 150 --ce_windowstep 100 > match.txt
rm *.bam *.sam *.bai &> /dev/null
python eval_ce_ins.py

exit $?
