# This file reads a sam file, and computes the C/E Statistic

import sys
import os
import math
import re
from read import Read
from misassemblyRegion import MisassemblyRegion
class CEStatistic:
   
    #initialize the class, do the initial read
    def __init__(self, input_file, winSize, winStep, t):
        self.input = input_file
        self.windowSize = winSize #size of the window
        self.windowStep = winStep # advancement of the window
        self.threshold = t #threshold for what we mark as bad
        self.fInput = open(self.input, 'r') #the input file
        self.count = 0 # the number of reads in the library
        self.libLength = 0
        self.libLenCount = 0
        self.libLenArray = []
        self.readArray = {} #store the reads by contig
        self.zScores = {} #scores for the different base pairs
        self.positions = {}
        self.misassemblies = []
        self.doParse()
        self.doProcess()
        

    def doParse(self):
        assert(self.fInput)

        #scrap the headers
        for x in range(0, 3):
            self.fInput.readline()
        

        for line in self.fInput:
            if self.count % 2 == 0:
                data = line.split('\t');
                length = math.fabs(int(data[8]));
                #enforce that length is between 0 and 1000
                if (length > 0) and (length < 1000):
                    self.libLength = self.libLength + length;
                    self.libLenCount = self.libLenCount + 1;
                    self.libLenArray.append(length)
                    pos = int(data[3]);
                    pnext = int(data[7]);
                    tlen = math.fabs(int(data[8]));
                    contig = data[2];
                    read = Read();
                    read.setPos(pos);
                    read.setContig(contig);
                    read.setPNext(pnext);
                    read.setLen(tlen);
                    read.setFinal();
                    if contig not in self.readArray:
                        self.readArray[contig] = {}
                    self.readArray[contig][pos] = read
        
            self.count = self.count + 1;

    
    def doCEStat(self, reads, libAvgLen, libAvgStd):
        m = 0
        for r in reads:
            # m = m + math.fabs((r.getPos() - r.getPNext()));
            m = m + math.fabs( r.getLen() )
        m = float(m)/(len(reads))


        z = float(m - libAvgLen)/(float(libAvgStd)/(math.sqrt( math.fabs(len(reads)) )))
        return z
    


    def doWindow(self, start, end, reads, libAvg, libStd, contig):
        #print "window end %d" % (end)
        window = []
        for r in self.positions[contig]:
            if reads[r].getPos() in range(start, end):
                window.append(reads[r])
                
        if( len(window) == 0 ):
            return;
        else:
            z = self.doCEStat(window, libAvg, libStd)
            if contig not in self.zScores:
                self.zScores[contig] = {}
 
        for r in window:
            if(r.getPos() not in self.zScores[contig]):
                self.zScores[contig][r.getPos()] = (0,0)
            self.zScores[contig][r.getPos()] = (self.zScores[contig][r.getPos()][0] + z, self.zScores[contig][r.getPos()][1]+1)

     
    def doProcess(self):
        meanDistance = float(self.libLength)/float(self.libLenCount);
        variance = 0;

        for dist in self.libLenArray:
            variance = variance + (dist - meanDistance)*(dist-meanDistance);
    
        variance = float(variance)/(self.libLenCount);
        standardDeviation = math.sqrt(variance);
        #print "The Library Mean Insert size is: %f" % (meanDistance)
        #print "The Library Standard Dev size is: %f" % (standardDeviation)
        #print "The libLenCount is: %f" % (self.libLenCount)
        
        output = open(sys.argv[2], 'w')
        positions = {}
        
        doingMisassembly = False #whether or not we have found the beginning of a misassembled region
        
        t = self.threshold 
        startLoc = 0
        endLoc = 0
        for contig in self.readArray.keys():
            self.positions[contig] = sorted(self.readArray[contig].keys())
            maximum = self.positions[contig][len(self.positions[contig])-1]
          #  print "The Max is %d" % (maximum)
            self.zScores[contig] = {}
            for i in range(0-self.windowSize, maximum+self.windowSize, self.windowStep):
                self.doWindow(i, i+self.windowSize, self.readArray[contig], meanDistance, standardDeviation, contig)
                
            for v in sorted(self.zScores[contig].keys()):
                if( ((float(self.zScores[contig][v][0])/self.zScores[contig][v][1]) >= t) or (float(self.zScores[contig][v][0])/self.zScores[contig][v][1]) <= (-1*t) ):
                    if(not doingMisassembly): #found the beginning of a misassembled region
                        doingMisassembly = True
                        startLoc = v
                        endLoc = v
                    else: # found the middle of a misassembled region
                        endLoc = v
                        
                else:
                    if(doingMisassembly): #end of misassembled region
                        doingMisassembly = False
         #               print "Contig: %s Start: %d | End %d" % (contig, startLoc, endLoc)
                        self.misassemblies.append(MisassemblyRegion(contig, startLoc, endLoc, "insertion/deletion", None))

    def getMisassemblies(self):
        return self.misassemblies
                                                  

                                                  
                    


#input = sys.argv[1]
#ce = CEStatistic(input, 150, 100, 1.2)