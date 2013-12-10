import random
import sys
from optparse import OptionParser


class Error(object):
    """docstring for Error"""
    def __init__(self, start,end, type, confidence):
        super(Error, self).__init__()
        self.start = start
        self.end = end
        self.type = type
        self.confidence = confidence

    def __init__(self,errorString):
        super(Error, self).__init__()
        errorString = errorString.split()
        self.start = int(errorString[1])
        self.end = int(errorString[2])
        self.type = errorString[3]
        self.confidence = int(errorString[4])
        

class Verifier(object):
    """docstring for Verifier"""
    def __init__(self):
        super(Verifier, self).__init__()
        self.errors = []

    def readOracle(self,o_file):
        with open(o_file,"w") as oracleFile:
            for errorLine in oracleFile:
                self.errors.append(Error(errorLine))

        



def main():
    parser = OptionParser()
    parser.add_option('-o',"--oracle-file",dest="oracle_file")
    parser.add_option("-r","--result-file", dest = "result_file")

    (options, args) = parser.parse_args()


if __name__ == '__main__':
    main()