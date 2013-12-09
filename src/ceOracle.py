# read the file.... checking to ensure that the program found misassemblies. 

import sys
import os
import math
import re
from ceStatistic import CEStatistic


#fInput = open(sys.argv[1], 'r')
winSize = (int(sys.argv[2]))
winStep = (int(sys.argv[3]))
statThreshold = (float(sys.argv[4]))
testThreshold = (float(sys.argv[5]))



ce = CEStatistic(sys.argv[1], winSize, winStep, statThreshold)
misassemblies = ce.getMisassemblies()
oracle = './oracle.txt';
fOracle = open(oracle, 'r');


totScores = 0;
sumScores = 0;

scores = {};
 
for line in fOracle:
    data = line.split('\t')
    index = int(data[0])
    length = int(data[1])
    mod = data[2].strip()
    done = False
    for i in range(index-testThreshold*length, index+testThreshold*length):
        if done:
            break;
        for m in misassemblies:
            if i in range(m.getStart(), m.getEnd()):
                print "Correctly Found Error at %d!" % index
                done = True
                break;
    if not done:
        print "Failed to find insertion at %d" % (index)
