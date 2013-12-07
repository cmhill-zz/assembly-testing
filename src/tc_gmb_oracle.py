#!/usr/bin/python

import argparse
import misassemblyRegion as mr

# Form misassembly region list from the contents of a file
def getmrlist(fname):
    mrlist = []
    with open(fname, "r") as f:
        for line in f:
            els = line.strip().split()
            mrlist.append(mr.MisassemblyRegion(els[0], int(els[1]), int(els[2]), els[3],None))
    return mrlist

# Check if misassembly regions are equivalent
def isEquivalent(mr1, mr2):
    if mr1.rname != mr2.rname:
        return False

    startPos = max(mr1.startPos, mr2.startPos)
    endPos = min(mr1.endPos, mr2.endPos)

    if startPos > endPos:
        return False
    
    regionLen = endPos - startPos + 1
    if (regionLen > (0.8 * mr1.getRegionLength())) and (regionLen > (0.8 * mr2.getRegionLength())):
        return True
    
    return False

parser = argparse.ArgumentParser(description="Oracle for feasibility test cases for good minus bad analysis")
parser.add_argument("--oracle", dest="oracleFile", required=True, type=str, help="file contains correct misassembly regions")
parser.add_argument("--result", dest="resultFile", required=True, type=str, help="file contains resultant misassembly regions of good-minus-bad analysis")
args = parser.parse_args()

resultmrlist = getmrlist(args.resultFile)
oraclemrlist = getmrlist(args.oracleFile)

# For each oracle misassembly regions check if there exists an equivalent misassembly region in resultant file
for oraclemr in oraclemrlist:
    foundEquivalent = False
    for resultmr in resultmrlist:
        if isEquivalent(oraclemr, resultmr):
            foundEquivalent = True
            break
    if not foundEquivalent:
        exit(1)
exit(0)
        
