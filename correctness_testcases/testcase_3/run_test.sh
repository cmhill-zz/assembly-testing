#! /usr/bin/sh

# For test cases which contain high-density repeats, it makes sense to lower the standard deviation multiplier
# (on tests that use one such metric), because the coverage itself will have a higher spread which we need to
# detect. To that end, we have decreased the standard deviation parameter in this test.

currwd=`pwd`;
cd ../../assembly-read-coverage/org/umd/assemblytest/readcoverage/
python clipper.py -a ../../../../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/testcases/test_003.assembly.fasta -r ../../../../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/testcases/test_003.reads.fasta -w 10 -s 1 -t Gaussian -p 2.0 
cd $currwd"/../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/"
python pythia.py -m ../../../../../../assembly-read-coverage/org/umd/assemblytest/readcoverage/out/test_003.W10_S1_Gaussian_P2.0_OVER_BP.cov -o testcases/test_003.oracle
pythiaFlag=$?
cd $currwd;
exit $pythiaFlag
