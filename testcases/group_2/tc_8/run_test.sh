#! /usr/bin/sh

python ../../src/matePairAnalysis.py --fasta lambda_virus_modified.fa -1 reads_1.fq -2 reads_2.fq  --gmb > result
rm *.sam *.bam *.bai &> /dev/null
python ../../src/tc_gmb_oracle.py --oracle oracle --result result

exit $?