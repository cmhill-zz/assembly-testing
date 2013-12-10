#!/usr/bin/python

import numpy as np
import os
import pysam
import misassemblyRegion as mr

from Bio import SeqIO

class GoodMinusBadScorer:
    # Initialize the GoodMinusBadScorer class
    def __init__(self, fastaFile, samFile):
        # assumption: assembly file is fasta
        self.fastaFile = fastaFile
        self.seqRecords = SeqIO.parse(self.fastaFile, "fasta")
        # assumption: alignment file is a bamfile
        self.samFile = samFile
        self.samFileParser = pysam.Samfile(self.samFile, "rb")
        self.avgMatePairLength = self.calculateAvgMatePairLength(self.samFileParser.fetch())

    # Calculate average lenght for mate-pairs which lies on the same contig.
    def calculateAvgMatePairLength(self, matePairReads):
        runningSum = 0
        matePairCount = 0

        # Normally, it is enough to go over only one pair of a mate-pair.
        # However, since we are taking the average it won't matter even if we take both ends into account.
        # This should be faster compared to the alternative.
        for matePairRead in matePairReads:
            # Check if this read is mapped and it actually has a mapped mate-pair
            if (not matePairRead.is_paired) or matePairRead.is_unmapped or matePairRead.mate_is_unmapped:
                continue

            # Check if mate-pairs lie on the same contig
            if not self.isInSameReference(matePairRead):
                continue

            # Count the valid number of mate pairs that will add up in the running sum for length
            matePairCount = matePairCount + 1

            # Add current mate-pair length to running sum
            runningSum = runningSum + abs(matePairRead.tlen)

        # We are not prepared against having division-by-zero case
        if matePairCount == 0:
            raise NotImplementedError("The case where no valid mate-pairs exists for average length calculation is not handled")

        # Return average mate-pair length
        return float(runningSum) / float(matePairCount)

    # Check if both ends of a mate-pair is in the same reference
    def isInSameReference(self, alignedRead):
        # assumption: reference should be represented as an integer for both mate-pair
        # this integer is a key to some mapping which maps the integer to reference name
        assert(type(alignedRead.tid) is int)
        assert(type(alignedRead.rnext) is int)

        return alignedRead.tid == alignedRead.rnext

    # Check if a mate pair length is bad or not
    def isBadPair(self, matePairLength):
        return abs(matePairLength) > 2 * self.avgMatePairLength
    
    # Get start and end position for a read. Read should be in the same contig
    def getRangeForRead(self, read):
        # Get the leftmost position of the mate-pair
        if(read.tlen < 0):
            startPos = read.pnext
        else:
            startPos = read.pos
                
        # Find the rightmost position of the mate-pair
        endPos = startPos + abs(read.tlen)
        assert(startPos <= endPos)

        return (startPos, endPos)

    def updateRangesAndScoresWithRead(self, partitionedRangeList, scoreDictionary, read):
        # Compute new partitions for overlapping ranges r1 and r2
        def computePartitionDict(r1, r2):
            partitionDict = {"out1": None, "in1": None, "overlap": None, "in2": None, "out2": None}
            if r2[0] < r1[0]:
                partitionDict["out1"] = (r2[0], r1[0])
                if r2[1] < r1[1]:
                    partitionDict["overlap"] = (r1[0], r2[1])
                    partitionDict["in2"] = (r2[1], r1[1])
                else:
                    partitionDict["overlap"] = r1
                    if r1[1] != r2[1]:
                        partitionDict["out2"] = (r1[1], r2[1])
            else:
                if r1[0] < r2[0]:
                    partitionDict["in1"] = (r1[0], r2[0])
                if r2[1] < r1[1]:
                    partitionDict["overlap"] = r2
                    partitionDict["in2"] = (r2[1], r1[1])
                else:
                    partitionDict["overlap"] = (r2[0], r1[1])
                    if r1[1] != r2[1]:
                        partitionDict["out2"] = (r1[1], r2[1])

            return partitionDict

        # Update range list
        def updatePartitionedRangeList(partitionedRangeList, index, partitionDict):
            newPartitionsInReverseOrder = [el for el in
                                           [partitionDict["in2"], partitionDict["overlap"], partitionDict["in1"], partitionDict["out1"]]
                                           if el != None]
            for newRangePartition in newPartitionsInReverseOrder:
                partitionedRangeList.insert(index, newRangePartition)

        # Update score dictionary
        def updateScoreDictionary(scoreDictionary, updateScore, currentRangeScore, partitionDict):
            if partitionDict["out1"]:
                scoreDictionary[partitionDict["out1"]] = updateScore
            if partitionDict["in1"]:
                scoreDictionary[partitionDict["in1"]] = currentRangeScore
            if partitionDict["overlap"]:
                scoreDictionary[partitionDict["overlap"]] = currentRangeScore + updateScore
            if partitionDict["in2"]:
                scoreDictionary[partitionDict["in2"]] = currentRangeScore

        # Do binary search on partitionedRangeList to figure out where to start comparing ranges
        def findStartingComparisonIndex(readRange, partitionedRangeList):
            start = 0
            end = len(partitionedRangeList)

            if end == 0:
                return 0
            
            while start < end:
                mid = (start + end) / 2
                range = partitionedRangeList[mid]

                if readRange[1] <= range[0]:
                    end = mid
                elif range[1] <= readRange[0]:
                    start = mid + 1
                else:
                    break

            while not (mid == 0 or readRange[1] <= range[0] or range[1] <= readRange[0]):
                mid = mid - 1
                range = partitionedRangeList[mid]

            return mid


        # If read is bad update with -1. Otherwise, update with 1
        if self.isBadPair(read.tlen):
            updateScore = -1
        else:
            updateScore = 1

        # Modify range list with the current read and compute new scores accordingly
        readRange = self.getRangeForRead(read)
        counter = findStartingComparisonIndex(readRange, partitionedRangeList)
        while counter < len(partitionedRangeList):
            range = partitionedRangeList[counter]
            if readRange[1] <= range[0]:
                partitionedRangeList.insert(counter, readRange)
                scoreDictionary[readRange] = updateScore
                readRange = None
                break
            elif range[1] <= readRange[0]:
                counter = counter + 1
                continue

            partitionedRangeList.pop(counter)
            currentRangeScore = scoreDictionary.pop(range)
            partitionDict = computePartitionDict(range, readRange)
            
            updatePartitionedRangeList(partitionedRangeList, counter, partitionDict)
            updateScoreDictionary(scoreDictionary, updateScore, currentRangeScore, partitionDict)

            if partitionDict["out2"]:
                readRange = partitionDict["out2"]
                counter = counter + 1
            else:
                readRange = None
                break

        # Handle the case where a range comes after every existing range
        if readRange:
            partitionedRangeList.append(readRange)
            scoreDictionary[readRange] = updateScore

    # Fill good minus bad score array according to range partition and their corresponding scores
    def computeScoreArray(self, goodMinusBadScoreArray, partitionedRangeList, scoreDictionary):
        for range in partitionedRangeList:
            score = scoreDictionary[range]
            for index in xrange(range[0], range[1]):
                goodMinusBadScoreArray[index] = score

    # Calculate good-minus-bad score for base-pairs in a specific reference
    def calculateScoreForReference(self, referenceName, referenceLength):
        # fetch all the reads aligned to the reference
        alignedReads = self.samFileParser.fetch(referenceName)

        # Initialize helper data structures
        scoreDictionary = {}
        partitionedRangeList = []
        for alignedRead in alignedReads:
            # Check if this read is mapped and it had actually a mapped mate
            if self.isInSameReference(alignedRead) and alignedRead.is_paired and not (alignedRead.is_unmapped or alignedRead.mate_is_unmapped):
                self.updateRangesAndScoresWithRead(partitionedRangeList, scoreDictionary, alignedRead)
            else:
                if int(os.environ.get('DEBUG', 0)) > 0:
                    raise NotImplementedError("The case where different ends of mate-pair aligns to different references haven't been handled yet.")

        # compute scoring array
        goodMinusBadScoreArray = np.zeros(referenceLength, dtype=int)
        self.computeScoreArray(goodMinusBadScoreArray, partitionedRangeList, scoreDictionary)

        # we divide by two since we count each mate-pair twice, one for each end.
        return goodMinusBadScoreArray / 2

    # Calculate good-minus-bad scores for base-pairs for each reference in the fasta file
    def calculateScore(self):
        scoreDict = {}
        self.seqRecords = SeqIO.parse(self.fastaFile, "fasta")
        for seqRecord in self.seqRecords:
            scoreDict[seqRecord.id] = self.calculateScoreForReference(seqRecord.id, len(seqRecord))

        return scoreDict

    # Find misassembly regions
    def findMisassemblyRegions(self):
        scoreDict = self.calculateScore()
        misassemblyRegions = []
        for key in scoreDict:
            scores = scoreDict[key]
            isNegativeRegion = False
            startPos = 0
            badPos = 0
            for index, score in enumerate(scores):
                if score < 0 and (not isNegativeRegion):
                    isNegativeRegion = not isNegativeRegion
                    startPos = index

                if score >= 0 and isNegativeRegion:
                    isNegativeRegion = not isNegativeRegion
                    endPos = index
                    misassemblyRegions.append(mr.MisassemblyRegion(key, startPos, endPos, "inversion", None))

            if isNegativeRegion:
                misassemblyRegions.append(mr.MisassemblyRegion(key, startPos, len(scores)-1, "inversion", None))

        return misassemblyRegions
