# read the file.... checking to ensure that the program found misassemblies. 

import sys
import os
import math
import re
input = 'ceValues'
fInput = open(sys.argv[1], 'r')


oracle = './oracle.txt';
fOracle = open(sys.argv[2], 'r');


totScores = 0;
sumScores = 0;

scores = {};
 

for line in fInput:
    data = line.split('\t');
    score = float(data[2]);
    point = int(data[0]);
    scores[point] = score


for line in fOracle:
    data = line.split('\t')
    index = int(data[0])
    length = int(data[1])
    mod = data[2].strip()
    
    for i in range(index-4*length, index+4*length):

        if mod == 'i':
            if i in scores:
                if(scores[i] < 1.5):
                    print "Correctly Found Insertion at %d!" % i
                    break;
                if(scores[i] > 1.5):
                    print "Correctly Found Error at %d!" % i
                    break;
        else:
            if i in scores:
                if(scores[i] > 1.5):
                    print "Correctly Found Deletion at %d!" % i
                    break;
                
                if(scores[i] < 1.5):
                    print "Correctly Found Error at %d!" % i
                    break;
                
