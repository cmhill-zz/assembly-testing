# This file reads a sam file, and computes the C/E Statistic

import sys
import os
import math
import re
from read import Read

#change this to read from ARGV
input = sys.argv[1];
windowSize = 25000
windowStep = 10000


fInput = open(input, 'r');
aInput = []; #we store the input lines here to avoid sys/calls to read

count = 0;
libLength = 0;
libLenCount = 0;
libLenArray = [];

readArray = {}

nameRE = re.compile('\d')
zScores = {}



def doCEStat(reads, libAvgLen, libAvgStd):
    m = 0
    #print "reads: %d" % (len(reads))
    for r in reads:
        # m = m + math.fabs((r.getPos() - r.getPNext()));
        m = m + math.fabs( r.getLen() )
    m = float(m)/(len(reads))


    #print "m = %f, libAvgLen = %f\n" % (m, libAvgLen)
    z = float(m - libAvgLen)/(float(libAvgStd)/(math.sqrt( math.fabs(len(reads)) )))
    return z
    


def doWindow(start, end, reads, libAvg, libStd):
    print "window end %d" % (end)
    window = []
    for r in positions:
        if readArray[r].getPos() in range(start, end):
            window.append(readArray[r])
    
    if( len(window) == 0 ):
        return;
    else:
        z = doCEStat(window, libAvg, libStd)
        for i in positions:
            if i in range(start, end):
                if(i not in zScores):
                    zScores[i] = (0, 0)
                zScores[i] = (zScores[i][0] + z, zScores[i][1]+ 1)



#scrap the headers
for x in range(0, 3):
    fInput.readline();


for line in fInput:
    if count % 2 == 0:
        data = line.split('\t');
        #length = math.fabs(int(data[8]));
        # we should probs check to see that the mate is from the same read
        length = math.fabs(int(data[8]));

        #enforce that length is between 0 and 1000
        if (length > 0) and (length < 1000):
            libLength = libLength + length;
            libLenCount = libLenCount + 1;
            libLenArray.append(length)
            #name = int(data[0][1::]);
            pos = int(data[3]);
            pnext = int(data[7]);
            tlen = math.fabs(int(data[8]));
            
            read = Read();
            read.setPos(pos);
            read.setPNext(pnext);
            #read.setName(name);
            read.setLen(tlen);
            read.setFinal();
            readArray[pos] = read
        

    count = count + 1;

meanDistance = float(libLength)/(libLenCount);
variance = 0;

for dist in libLenArray:
    variance = variance + (dist - meanDistance)*(dist-meanDistance);
    
variance = float(variance)/(libLenCount);
standardDeviation = math.sqrt(variance);
print "The Library Mean Insert size is: %f" % (meanDistance)
print "The Library Standard Dev size is: %f" % (standardDeviation)
print "The libLenCount is: %f" % (libLenCount)
positions = sorted(readArray.keys())
maximum = positions[len(positions)-1]
print(maximum) 

for i in range(0-windowSize, maximum+windowSize, windowStep):
    doWindow(i, i+windowSize, readArray, meanDistance, standardDeviation);

output = open(sys.argv[2], 'w')
vals = sorted(zScores.keys())
for v in vals:
    if(v >= 0):
        output.write(str(v))
        output.write('\t\t')
        output.write(str(zScores[v][0]/zScores[v][1]))
        output.write('\n')
output.close()

