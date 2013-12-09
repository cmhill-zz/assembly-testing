import os
import sys
sys.path.insert(0, '../../../src')

import oracleTester
import gaussianCheck
import genAsblyAndOrcl

matchGaussian = 'match.txt'
oracleLocation = 'oracle'
accuracyLocation = 'result.txt'

oracleTester.testOracle(matchGaussian, oracleLocation, accuracyLocation)
