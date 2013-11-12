import os
import ../../src/oracleTester
import ../../src/gaussianCheck
import ../../src/genAsblyAndOrcl

orgSq = 'testcases/tc_gau_ins/data.txt'
ipSq = 'testcases/tc_gau_ins/dataMod.txt'
outputIndex = 'testcases/tc_gau_ins/modIndex'
read1 = 'testcases/tc_gau_ins/r1.fq'
read2 = 'testcases/tc_gau_ins/r2.fq'
outputMatchBowtie = 'testcases/tc_gau_ins/output.sam'
matchGaussian = 'testcases/tc_gau_ins/match.txt'
oracleLocation = 'testcases/tc_gau_ins/oracle.txt'

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


orgSq = 'testcases/tc_gau_del/data.txt'
ipSq = 'testcases/tc_gau_del/dataMod.txt'
outputIndex = 'testcases/tc_gau_del/modIndex'
read1 = 'testcases/tc_gau_del/r1.fq'
read2 = 'testcases/tc_gau_del/r2.fq'
outputMatchBowtie = 'testcases/tc_gau_del/output.sam'
matchGaussian = 'testcases/tc_gau_del/match.txt'
oracleLocation = 'testcases/tc_gau_del/oracle.txt'

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



orgSq = 'testcases/tc_gau_ins_del/data.txt'
ipSq = 'testcases/tc_gau_ins_del/dataMod.txt'
outputIndex = 'testcases/tc_gau_ins_del/modIndex'
read1 = 'testcases/tc_gau_ins_del/r1.fq'
read2 = 'testcases/tc_gau_ins_del/r2.fq'
outputMatchBowtie = 'testcases/tc_gau_ins_del/output.sam'
matchGaussian = 'testcases/tc_gau_ins_del/match.txt'
oracleLocation = 'testcases/tc_gau_ins_del/oracle.txt'

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
