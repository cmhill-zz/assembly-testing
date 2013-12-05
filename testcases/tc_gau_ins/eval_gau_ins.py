import os
import sys
sys.path.insert(0, '../../src')

import oracleTester
import gaussianCheck
import genAsblyAndOrcl

orgSq = 'data.txt'
ipSq = 'dataMod.txt'
outputIndex = 'modIndex'
read1 = 'r1.fq'
read2 = 'r2.fq'
outputMatchBowtie = 'output.sam'
matchGaussian = 'match.txt'
oracleLocation = 'oracle.txt'
accuracyLocation = 'result.txt'

#generate sequence
#genAsblyAndOrcl.generateValidation(orgSq, ipSq, oracleLocation, True, False)

#generate reads
#os.system('wgsim -1 40 -2 40 -R 0.0 -X 0.0 -e 0.0 -N 10000 -d 200 -s 0 ' + orgSq + ' ' + read1 + ' ' + read2 + ' >/dev/null')

#build index
#os.system('bowtie2-build ' + ipSq + ' ' + outputIndex + ' >/dev/null')

#align reads
#os.system('bowtie2 -x ' + outputIndex + ' -1 ' + read1 + ' -2 ' + read2 + ' -S ' + outputMatchBowtie + ' >/dev/null')

#evaluate the alignment using mate pair criterion
gaussianCheck.gCk(outputMatchBowtie, matchGaussian, 40)

oracleTester.testOracle(matchGaussian, oracleLocation, accuracyLocation)
