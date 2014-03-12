#! /usr/bin/sh

currwd=`pwd`;
cd assembly-read-coverage/org/umd/assemblytest/readcoverage/
python clipper.py -a ../../../../../data/influenza-A/influenza-A.assembly.fasta -r ../../../../../data/influenza-A/influenza-A.sequences.fasta -w 20 -s 1 -t Gaussian -p 2.0 
cd $currwd;
exit 0
