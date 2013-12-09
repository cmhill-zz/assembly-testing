#!/usr/bin/python

import argparse
import hashlib
import os
import time

def createSAM(fastaFileName, reads1, reads2, baseName, samFileName):
    os.system("bowtie2-build %s %s &> /dev/null" % (fastaFileName, baseName))
    if samFileName.endswith(".sam"):
        if reads1.endswith(".fasta"):
            os.system("bowtie2 -f -x %s -1 %s -2 %s -S %s &> /dev/null" % (baseName, reads1, reads2, samFileName))
        else:
            os.system("bowtie2 -x %s -1 %s -2 %s -S %s &> /dev/null" % (baseName, reads1, reads2, samFileName))
    else:
        if reads1.endswith(".fasta"):
            os.system("bowtie2 -f -x %s -1 %s -2 %s -S %s.sam &> /dev/null" % (baseName, reads1, reads2, samFileName))
        else:
            os.system("bowtie2 -x %s -1 %s -2 %s -S %s.sam &> /dev/null" % (baseName, reads1, reads2, samFileName))

    os.system("rm %s.*" % (baseName,))

def createBAM(samFileName, bamFileName):
    os.system("samtools view -bS %s > %s 2> /dev/null" % (samFileName, bamFileName))

def createSortedBAM(bamFileName, sortedBamFileNamePrefix):
    os.system("samtools sort %s %s &> /dev/null" % (bamFileName, sortedBamFileNamePrefix))

def createBAI(sortedBamFileName):
    os.system("samtools index %s &> /dev/null" % (sortedBamFileName))

def createRandomNamesDict():
    h = hashlib.md5()
    h.update(str(time.time()))
    baseName = h.hexdigest()

    h.update("SAM")
    samFileName = h.hexdigest() + ".sam"
    bamFileName = samFileName.replace(".sam", ".bam")
    randomNamesDict = {
        "baseName": baseName,
        "samFileName": samFileName,
        "bamFileName": bamFileName,
        "sortedBamFileNamePrefix": bamFileName.replace(".bam", ".sorted"),
        "sortedBamFileName": bamFileName.replace(".bam", ".sorted") + ".bam",
        "bamIndexFileName": bamFileName.replace(".bam", ".sorted") + ".bam.bai" 
        }

    return randomNamesDict

parser = argparse.ArgumentParser(description="Software to find misassemblies by doing mate-pair analysis." +
                                 " If any of the analysis flag is provided, only those analysis will be executed." +
                                 " Otherwise, all of the analysis will be executed.")
parser.add_argument("--fasta", dest="fastaFileName", required=True, help="fasta file name holding genome reference sequences")
parser.add_argument("-1", dest="readFile1", required=True, help="first part of the mate-pair reads")
parser.add_argument("-2", dest="readFile2", required=True, help="second part of the mate-pair reads")
parser.add_argument("--gmb", dest="gmb", action="store_true", help="if present, do only good minus bad analysis.")
parser.add_argument("--ce", dest="ce", action="store_true", help="if present, do only ce Statistic")
parser.add_argument("--gau", dest="gau", action="store_true", help="if present, do only gaussian analysis")
parser.add_argument("--gau_multiplier", dest="multiplier", default=4, type=int, help="this is used in gau analysis. it is the variance multiplier.")
parser.add_argument("--ce_windowsize", dest="windowSize", default=150, type=int, help="This is used in CE Statistic; controls the window size for the moving window average.")
parser.add_argument("--ce_windowstep", dest="windowStep", default=100, type=int, help="this is used in CE Statistic; controls the window step size for the moving window average.")
parser.add_argument("--ce_threshold", dest="threshold", default=1.2, type=float, help="this is used in CE Statistic; controls the theshold for marking regions as bad.")

args = parser.parse_args()

# Create random names that we will use as file names for sam/bam/index
randomNamesDict = createRandomNamesDict()

# TODO: We can update random names dictionary with user provided values if we want

# Create necessary files
createSAM(args.fastaFileName, args.readFile1, args.readFile2, randomNamesDict["baseName"], randomNamesDict["samFileName"])
createBAM(randomNamesDict["samFileName"], randomNamesDict["bamFileName"])
createSortedBAM(randomNamesDict["bamFileName"], randomNamesDict["sortedBamFileNamePrefix"])
createBAI(randomNamesDict["sortedBamFileName"])

# If non of the flags are set, set all the flags
if not (args.gmb or args.gau or args.ce):
    args.gmb = True
    args.gau = True
    args.ce = True

misassemblyRegionList = []
if args.gmb:
    import gmb
    g = gmb.GoodMinusBadScorer(args.fastaFileName, randomNamesDict["sortedBamFileName"])
    misassemblyRegionList = g.findMisassemblyRegions()

if args.gau:
    import gaussianCheck
    gaussianErrorList = gaussianCheck.gCk(randomNamesDict["samFileName"], args.multiplier)
    misassemblyRegionList.extend(gaussianErrorList)

if args.ce:
    import ceStatistic
    ce = ceStatistic.CE(randomNamesDict["samFileName"], args.windowSize, args.windowStep, args.threshold)
    ce_result = ce.getMisassemblies()
    misassemblyRegionList.extend(ce_result)

for misassemblyRegion in misassemblyRegionList:
    print str(misassemblyRegion)
