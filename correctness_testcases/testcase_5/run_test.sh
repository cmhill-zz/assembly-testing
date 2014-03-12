#! /usr/bin/bash

# For this testcase, it made sense to lower the window size.
currwd=`pwd`;
cd ../../assembly-read-coverage/org/umd/assemblytest/readcoverage/
python clipper.py -a ../../../../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/testcases/test_005.assembly.fasta -r ../../../../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/testcases/test_005.reads.fasta -w 5 -s 1 -t Gaussian -p 5.0 
cd $currwd"/../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/"
python pythia.py -m ../../../../../../assembly-read-coverage/org/umd/assemblytest/readcoverage/out/test_005.W5_S1_Gaussian_P5.0_OVER_BP.cov -o testcases/test_005.oracle
pythiaFlag=$?
cd $currwd;
exit $pythiaFlag
