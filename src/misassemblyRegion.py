#!/usr/bin/python

class MisassemblyRegion():
    def __init__(self, rname, startPos, endPos, misassemblyType):
        self.rname = rname
        self.startPos = startPos
        self.endPos = endPos
        assert(self.startPos <= self.endPos)
        self.misassemblyType = misassemblyType

    def __repr__(self):
        return "%s\t%s\t%s\t%s" % (self.rname, str(self.startPos), str(self.endPos), self.misassemblyType)

    def __str__(self):
        return "%s\t%s\t%s\t%s" % (self.rname, str(self.startPos), str(self.endPos), self.misassemblyType)

    def getRegionLength(self):
        return self.endPos - self.startPos + 1
