#!/usr/bin/python

import pysam
import numpy as np
from Bio import SeqIO

class GoodMinusBadScorer:
    def __init__(self, fastaFile, samFile):
        # assumption: assembly file is fasta
        self.fastaFile = fastaFile
        self.seqRecords = SeqIO.parse(self.fastaFile, "fasta")
        # assumption: alignment file is a samfile
        self.samFile = samFile
        self.samFileParser = pysam.Samfile(self.samFile, "r")
        self.avgMatePairLength = self.calculateAvgMatePairLength(self.samFileParser.fetch())

    # Calculate average lenght for mate-pairs which lies on the same contig.
    def calculateAvgMatePairLength(self, matePairReads):
        runningSum = 0
        matePairCount = 0

        # Normally, it is enough to go over only one pair of a mate-pair.
        # However, since we are taking the average it won't matter even if we take both ends into account.
        # This should be faster compared to the alternative.
        for matePairRead in matePairReads:
            # Check if this read is actually has a mate-pair
            if not matePairRead.is_paired:
                continue

            # Check if mate-pairs lie on the same contig
            if not self.isInSameConting(matePairRead):
                continue
    
            matePairCount = matePairCount + 1
            runningSum = runningSum + abs(matePairRead.tlen)

        if matePairCount == 0:
            raise NotImplementedError("The case where no valid mate-pairs exists for average length calculation is not handled")

        return float(runningSum) / float(matePairCount)

    def isInSameContig(self, alignedRead):
        # assumption: reference should be represented as an integer for both mate-pair
        # this integer is a key to some mapping which maps the integer to reference name
        assert(type(alignedRead.tid) is int)
        assert(type(alignedRead.rnext) is int)

        return alignedRead.tid == alignedRead.rnext

    def isBadPair(self, matePairLength):
        return matePairLength > 2 * self.avgMatePairLength

    def calculateScoreForReference(self, referenceName, referenceLength):
        # initiliaze scoring array
        goodMinusBadScoreArray = np.zeros(referenceLength)

        # fetch all the reads aligned to the reference
        alignedReads = self.samFileParser.fetch(referenceName)

        for alignedRead in alignedReads:
            # Check if this read is actually a mate-pair
            if alignedRead.is_paired:
                # First, check if this is a bad pair
                # Otherwise treat it as a good pair as long as both ends in the same contig.
                # Note that inter-contig pairs can never be good pairs
                if self.isBadPair(alignedRead.tlen):
                    pass
                elif self.isInSameContig(alignedRead):
                    pass

        # we divide by two since we count each mate-pair twice, one from each end.
        return goodMinusBadScoreArray / 2

    def calculateScore(self):
        scoreDict = {}
        self.seqRecords = SeqIO.parse(self.fastaFile, "fasta")
        for seqRecord in self.seqRecords:
            scoreDict[seqRecord.id] = self.calculateScoreForReference(seqRecord.id, len(seqRecord))



            
            
                      
