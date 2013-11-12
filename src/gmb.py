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

    # Add appropriate score to base-pair locations corresponds to where read is aligned
    def addScore(self, arr, read):
        if self.isInSameReference(read):
            # Determine the score: -1 for bad, 1 for good
            if self.isBadPair(read.tlen):
                score = -1
            else:
                score = 1

            # Get the leftmost position of the mate-pair
            if(read.tlen < 0):
                startPos = read.pnext
            else:
                startPos = read.pos
                
            # Find the rightmost position of the mate-pair
            endPos = startPos + abs(read.tlen)

            assert(startPos <= endPos)

            # Add score to the indices from leftmost to rightmost
            for index in xrange(startPos, endPos):
                arr[index] = arr[index] + score
        else:
            if int(os.environ.get('DEBUG', 0)) > 0:
                raise NotImplementedError("The case where different ends of mate-pair aligns to different references haven't been handled yet.")

    # Calculate good-minus-bad score for base-pairs in a specific reference
    def calculateScoreForReference(self, referenceName, referenceLength):
        # initiliaze scoring array
        goodMinusBadScoreArray = np.zeros(referenceLength)

        # fetch all the reads aligned to the reference
        alignedReads = self.samFileParser.fetch(referenceName)

        for alignedRead in alignedReads:
            # Check if this read is mapped and it had actually a mapped mate
            if alignedRead.is_paired and not (alignedRead.is_unmapped or alignedRead.mate_is_unmapped):
                self.addScore(goodMinusBadScoreArray, alignedRead)

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
                    misassemblyRegions.append(mr.MisassemblyRegion(key, startPos, endPos, "inversion"))

            if isNegativeRegion:
                misassemblyRegions.append(mr.MisassemblyRegion(key, startPos, len(scores)-1, "inversion"))

        return misassemblyRegions
