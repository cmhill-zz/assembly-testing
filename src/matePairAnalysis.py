#!/usr/bin/python

import argparse
import gmb

parser = argparse.ArgumentParser(description="Software to find misassemblies by doing mate-pair analysis")
parser.add_argument("--fasta", dest="fastaFileName", required=True, help="fasta file name holding genome reference sequences")
parser.add_argument("-1", dest="readFile1", required=True, help="first part of the mate-pair reads")
parser.add_argument("-2", dest="readFile2", required=True, help="second part of the mate-pair reads")
parser.add_argument("--gmb", dest="bamFileName", default=None, help="if present, do good minus bad analysis. this should be a sorted and indexed BAM file.")

args = parser.parse_args()

misassemblyRegionList = []
if args.bamFileName != None:
    g = gmb.GoodMinusBadScorer(args.fastaFileName, args.bamFileName)
    misassemblyRegionList = g.findMisassemblyRegions()


for misassemblyRegion in misassemblyRegionList:
    print str(misassemblyRegion)
