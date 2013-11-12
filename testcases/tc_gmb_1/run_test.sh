#! /usr/bin/sh

python ../../src/matePairAnalysis.py --fasta lambda_virus_modified.fa -1 ../../data/lambda_virus/reads_1.fq -2 ../../data/lambda_virus/reads_2.fq  --gmb eg2-sorted.bam > result
python ../../src/tc_gmb_oracle.py --oracle oracle --result result

exit $?