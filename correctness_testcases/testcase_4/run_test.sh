#! /usr/bin/bash

currwd=`pwd`;
cd ../../assembly-read-coverage/org/umd/assemblytest/readcoverage/
python clipper.py -a ../../../../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/testcases/test_004.assembly.fasta -r ../../../../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/testcases/test_004.reads.fasta -w 10 -s 1 -t Gaussian -p 5.0 
cd $currwd"/../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/"
python pythia.py -m ../../../../../../assembly-read-coverage/org/umd/assemblytest/readcoverage/out/test_004.W10_S1_Gaussian_P5.0_OVER_BP.cov -o testcases/test_004.oracle
pythiaFlag=$?
cd $currwd;
exit $pythiaFlag
