#!/bin/bash

python ../../src/matePairAnalysis.py --ce --fasta insTest.fasta -1 r1.fq -2 r2.fq --ce_theshold 1.2 --ce_windowsize 150 --ce_windowstep 100 > results.txt

exit 0
