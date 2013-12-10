# read the file.... checking to ensure that the program found misassemblies. 

import sys
import os
import math
import re
from ceStatistic import CEStatistic


#fInput = open(sys.argv[1], 'r')

oracle = './oracle.txt'
fOracle = open(oracle, 'r')
fResults = open('./results.txt', 'r')

testThreshold = int(sys.argv[2])

totScores = 0
sumScores = 0

scores = {}
results = []




for line in fResults:
    data = line.split()
    contig_name = data[0]
    start = int(data[1])
    end = int(data[2])
    error_type = data[3]
    confidence_value = data[4]
    results.append( (contig_name, start, end) )



for line in fOracle:
    data = line.split()
    index = int(data[0])
    length = int(data[1])
    mod = data[2].strip()
    done = False
    

    for i in range(index-testThreshold*length, index+testThreshold*length):
        if done:
            break;
        for m in results:
            if i in range(m[1], m[2]):
                #print "Correctly Found Error at %d!" % index
                done = True
                break;
    if not done:
        #print "Failed to find insertion at %d" % (index)
        exit(1)


exit(0)
