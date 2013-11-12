import os
import oracleTester
import gaussianCheck
import genAsblyAndOrcl

orgSq = 'testcases/tc_gaussian/insert/data.txt'
ipSq = 'testcases/tc_gaussian/insert/dataMod.txt'
outputIndex = 'testcases/tc_gaussian/insert/modIndex'
read1 = 'testcases/tc_gaussian/insert/r1.fq'
read2 = 'testcases/tc_gaussian/insert/r2.fq'
outputMatchBowtie = 'testcases/tc_gaussian/insert/output.sam'
matchGaussian = 'testcases/tc_gaussian/insert/match.txt'
oracleLocation = 'testcases/tc_gaussian/insert/oracle.txt'

#generate sequence
genAsblyAndOrcl.generateValidation(orgSq, ipSq, oracleLocation, True, False)

#generate reads
os.system('wgsim -1 40 -2 40 -R 0.0 -X 0.0 -e 0.0 -N 10000 -d 200 -s 0 ' + orgSq + ' ' + read1 + ' ' + read2 + ' >/dev/null')

#build index
os.system('bowtie2-build ' + ipSq + ' ' + outputIndex + ' >/dev/null')

#align reads
os.system('bowtie2 -x ' + outputIndex + ' -1 ' + read1 + ' -2 ' + read2 + ' -S ' + outputMatchBowtie + ' >/dev/null')

#evaluate the alignment using mate pair criterion
gaussianCheck.gCk(outputMatchBowtie, matchGaussian, 40)

oracleTester.testOracle(matchGaussian, oracleLocation)


orgSq = 'testcases/tc_gaussian/delete/data.txt'
ipSq = 'testcases/tc_gaussian/delete/dataMod.txt'
outputIndex = 'testcases/tc_gaussian/delete/modIndex'
read1 = 'testcases/tc_gaussian/delete/r1.fq'
read2 = 'testcases/tc_gaussian/delete/r2.fq'
outputMatchBowtie = 'testcases/tc_gaussian/delete/output.sam'
matchGaussian = 'testcases/tc_gaussian/delete/match.txt'
oracleLocation = 'testcases/tc_gaussian/delete/oracle.txt'

#generate sequence
genAsblyAndOrcl.generateValidation(orgSq, ipSq, oracleLocation, False, True)

#generate reads
os.system('wgsim -1 40 -2 40 -R 0.0 -X 0.0 -e 0.0 -N 10000 -d 200 -s 0 ' + orgSq + ' ' + read1 + ' ' + read2 + ' >/dev/null')

#build index
os.system('bowtie2-build ' + ipSq + ' ' + outputIndex + ' >/dev/null')

#align reads
os.system('bowtie2 -x ' + outputIndex + ' -1 ' + read1 + ' -2 ' + read2 + ' -S ' + outputMatchBowtie + ' >/dev/null')

#evaluate the alignment using mate pair criterion
gaussianCheck.gCk(outputMatchBowtie, matchGaussian, 40)

oracleTester.testOracle(matchGaussian, oracleLocation)



orgSq = 'testcases/tc_gaussian/insAndDel/data.txt'
ipSq = 'testcases/tc_gaussian/insAndDel/dataMod.txt'
outputIndex = 'testcases/tc_gaussian/insAndDel/modIndex'
read1 = 'testcases/tc_gaussian/insAndDel/r1.fq'
read2 = 'testcases/tc_gaussian/insAndDel/r2.fq'
outputMatchBowtie = 'testcases/tc_gaussian/insAndDel/output.sam'
matchGaussian = 'testcases/tc_gaussian/insAndDel/match.txt'
oracleLocation = 'testcases/tc_gaussian/insAndDel/oracle.txt'

#generate sequence
genAsblyAndOrcl.generateValidation(orgSq, ipSq, oracleLocation, True, True)

#generate reads
os.system('wgsim -1 40 -2 40 -R 0.0 -X 0.0 -e 0.0 -N 10000 -d 200 -s 0 ' + orgSq + ' ' + read1 + ' ' + read2 + ' >/dev/null')

#build index
os.system('bowtie2-build ' + ipSq + ' ' + outputIndex + ' >/dev/null')

#align reads
os.system('bowtie2 -x ' + outputIndex + ' -1 ' + read1 + ' -2 ' + read2 + ' -S ' + outputMatchBowtie + ' >/dev/null')

#evaluate the alignment using mate pair criterion
gaussianCheck.gCk(outputMatchBowtie, matchGaussian, 40)

oracleTester.testOracle(matchGaussian, oracleLocation)
