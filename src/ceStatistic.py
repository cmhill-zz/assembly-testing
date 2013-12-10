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

        for line in self.fInput:
            data = line.split('\t')
            if(len(data) < 9):
                continue

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
        
        positions = {}
        
        doingMisassembly = False #whether or not we have found the beginning of a misassembled region
        
        t = self.threshold 
        startLoc = 0
        endLoc = 0
        doingMisassemblyType = None
        for contig in self.readArray.keys():
            self.positions[contig] = sorted(self.readArray[contig].keys())
            maximum = self.positions[contig][len(self.positions[contig])-1]
          #  print "The Max is %d" % (maximum)
            self.zScores[contig] = {}
            for i in range(0-self.windowSize, maximum+self.windowSize, self.windowStep):
                self.doWindow(i, i+self.windowSize, self.readArray[contig], meanDistance, standardDeviation, contig)
                
            for v in sorted(self.zScores[contig].keys()):
                if( ((float(self.zScores[contig][v][0])/self.zScores[contig][v][1]) >= t) ):
                    if(doingMisassembly and doingMisassemblyType == "insertion"): #already doing the correct type...
                        endLoc = v
                    elif(doingMisassembly and doingMisassemblyType == "deletion"): #doing a misassembly, but not right type...
                        self.misassemblies.append(MisassemblyRegion(contig, startLoc, endLoc, doingMisassemblyType, None)) #end the current region...
                        startLoc = v
                        endLoc = v
                        doingMisassemblyType = "insertion"
                    else:
                        doingMisassembly = True
                        doingMisassemblyType = "insertion"
                        startLoc = v
                        endLoc = v
                elif( (float(self.zScores[contig][v][0])/self.zScores[contig][v][1]) <= (-1*t) ):
                    if(doingMisassembly and doingMisassemblyType == "deletion"):
                        endLoc = v
                    elif(doingMisassembly and doingMisassemblyType == "insertion"):
                        self.misassemblies.append(MisassemblyRegion(contig, startLoc, endLoc, doingMisassemblyType, None)) #end the current region...
                        startLoc = v
                        endLoc = v
                        doingMisassemblyType = "deletion"
                    else:
                        doingMisassembly = True
                        doingMisassemblyType = "deletion"
                        startLoc = v
                        endLoc = v
                else:
                    if(doingMisassembly):
                        self.misassemblies.append(MisassemblyRegion(contig, startLoc, endLoc, doingMisassemblyType, None))
                    doingMisassembly = False
                    doingMisassemblyType == None

    def getMisassemblies(self):
        #for m in self.misassemblies:
            #print "%s\t\t%d\t%d\t%s" % (m.getName(), m.getStart(), m.getEnd(), m.getType())
        return self.misassemblies
                                                  

                                                  
                    


#input = sys.argv[1]
#ce = CEStatistic(input, 150, 100, 1.5)
#ce.getMisassemblies()
