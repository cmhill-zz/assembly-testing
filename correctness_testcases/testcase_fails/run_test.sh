#! /usr/bin/sh

# This test has been tuned for failure, because we are using an inappropriately large standard deviation parameter.
# When a test fails, "pythia" returns 1, and so do we.

currwd=`pwd`;
cd ../../assembly-read-coverage/org/umd/assemblytest/readcoverage/
python clipper.py -a ../../../../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/testcases/test_003.assembly.fasta -r ../../../../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/testcases/test_003.reads.fasta -w 10 -s 1 -t Gaussian -p 8.0 
cd $currwd"/../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/"
python pythia.py -m ../../../../../../assembly-read-coverage/org/umd/assemblytest/readcoverage/out/test_003.W10_S1_Gaussian_P8.0_OVER_BP.cov -o testcases/test_003.oracle
pythiaFlag=$?
cd $currwd;
exit $pythiaFlag
