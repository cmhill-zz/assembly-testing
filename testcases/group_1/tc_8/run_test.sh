#! /usr/bin/sh

rm -rf ./out/*;
python ../../../assembly-read-coverage/org/umd/assemblytest/readcoverage/clipper.py -a assembly.fasta -r reads.fasta -w 50000 -s 1 -t Gaussian -p 1.4
rm -rf ./out/*.sam ./out/*.bt2 ./out/*.stdout ./out/*.stderr
python ../../../assembly-read-coverage-test/test/org/umd/assemblytest/readcoverage/pythia.py -m ./out/*_OVER_BP.cov -o oracle.oracle > pythia.stdout
cat pythia.stdout 
pythiaFlag=$?
exit $pythiaFlag
