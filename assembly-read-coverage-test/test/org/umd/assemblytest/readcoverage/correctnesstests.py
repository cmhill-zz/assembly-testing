import math
import random
import sys

# Produces random assemblies, and reads with duplicates in certain regions of
# those assemblies. Our error detection should then detect duplicates in those
# regions of the assembly in which duplicates were introduced
class CorrectnessTests:

    def __init__(self):
        self.assembly = []
        self.reads = []
        self.readnamestart = 10000000

    # Generates contigcount number of contigs of an assembly, where each contig
    # is of length length
    # returns: an array of contigs, each a string of a, t, c, and g's.
    def gen_assembly(self, contigcount, length):
        self.assembly = []
        for s in range(contigcount):
            self.assembly.append("".join([random.choice(['a','t','c','g']) for i in range(length)]))

        return self.assembly

    # Generates reads corresponding to the generated assembly.
    # readlen: the length of reads to produce
    #   note - some reads will be shorter if contig length is not a multiple of readlen
    # repeatcoords: list of tuples designating repeat locations, (contig, startpos)
    # returns: an array of strings of reads
    def gen_reads(self, readlen, repeatcoords):
        self.reads = []

        # cover assembly
        for contig in self.assembly:
            readcount = int(math.ceil(1.0*len(contig)/readlen))
            for pos in [i*readlen for i in range(readcount)]:
                self.reads.append(contig[pos:min(pos+readlen, len(contig))])
                self.reads.append(contig[max(0,pos-(readlen/2)):min(pos-(readlen/2)+readlen, len(contig))]) # integer division
                if pos+readlen >= len(contig) and pos-(readlen/2)+readlen < len(contig):
                    self.reads.append(contig[pos-(readlen/2)+readlen:len(contig)])

        # insert repeats
        for repeat in repeatcoords:
            contig = self.assembly[repeat[0]]
            self.reads.append(contig[repeat[1]:repeat[2]])
            self.reads.append(contig[repeat[1]:repeat[2]])

        return self.reads

    # Writes the last assembly generated to the given file
    def write_assembly(self, filename):
        f = open(filename, 'w')
        for i in range(len(self.assembly)):
            f.write(">" + str(i+1) + "\n")
            f.write(self.assembly[i] + "\n")
        f.close()

    # Writes the last set of reads generated to the given file
    def write_reads(self, filename):
        f = open(filename, 'w')
        for i in range(len(self.reads)):
            f.write(">" + str(i+self.readnamestart) + "\n")
            f.write(self.reads[i] + "\n")
        f.close()

if __name__ == "__main__":
    tests = CorrectnessTests()

#    tests.gen_assembly(1,15)
#    tests.gen_reads(5,[])
#    tests.write_assembly("assembly_test_001")
#    tests.write_reads("reads_test_001")
#
#    sys.exit(0)

    # test 1: no duplicates
    # novelty: no duplicates
    # how generated: 4 contigs each of length 500bp
    tests.gen_assembly(4, 500)
    tests.gen_reads(100,[])
    tests.write_assembly("./testcases/test_001.assembly.fasta")
    tests.write_reads("./testcases/test_001.reads.fasta")
    f = open("./testcases/test_001.oracle", "w")
    f.write(">1\n" + "0"*500 + "\n>2\n" + "0"*500 + "\n>3\n" + "0"*500 + "\n>4\n" + "0"*500)
    f.close()

    # test 2: small duplicate
    # novelty: has small segment with single duplicate, our method should detect this.
    # how generated: 4 contigs each of length 500bp, in contig 1, base pairs 100-120 are repeated.
    tests.gen_assembly(4, 500)
    tests.gen_reads(100,[(0,100, 120)])
    tests.write_assembly("./testcases/test_002.assembly.fasta")
    tests.write_reads("./testcases/test_002.reads.fasta")
    f = open("./testcases/test_002.oracle", "w")
    f.write(">1\n" + "0"*100 + "1"*20 + "0"*380 + "\n>2\n" + "0"*500 + "\n>3\n" + "0"*500 + "\n>4\n" + "0"*500)
    f.close()

    # test 3: big duplicate
    # novelty: has big segment with single duplicate, our method should also detect large duplicates.
    # how generate: 4 contigs each of length 500bp, in contig 1, base pairs 100-300 are repeated.
    tests.gen_assembly(4, 500)
    tests.gen_reads(100,[(0,100,300)])
    tests.write_assembly("./testcases/test_003.assembly.fasta")
    tests.write_reads("./testcases/test_003.reads.fasta")
    f = open("./testcases/test_003.oracle", "w")
    f.write(">1\n" + "0"*100 + "1"*200 + "0"*200 + "\n>2\n" + "0"*500 + "\n>3\n" + "0"*500 + "\n>4\n" + "0"*500)
    f.close()

    # test 4: multiple small duplicates, far apart
    # novelty: Multiple duplicates. Our method should be capable of finding more than single duplicates.
    # how generate: 4 contigs each of length 500bp, in contig 1, base pairs 50-75 and 450-475 are repeated.
    tests.gen_assembly(4, 500)
    tests.gen_reads(100,[(0,50,75), (0,450,475)])
    tests.write_assembly("./testcases/test_004.assembly.fasta")
    tests.write_reads("./testcases/test_004.reads.fasta")
    f = open("./testcases/test_004.oracle", "w")
    f.write(">1\n" + "0"*50 + "1"*25 + "0"*375 + "1"*25 + "0"*25 + "\n>2\n" + "0"*500 + "\n>3\n" + "0"*500 + "\n>4\n" + "0"*500)
    f.close()

    # test 5: multiple small duplicates, close together
    # novelty: Multiple duplicates, with close proximity. Our method should detect duplicates even when close together.
    # how generate: 4 contigs each of length 500bp, in contig 1, base pairs 50-75 and 85-110 are repeated.
    tests.gen_assembly(4, 500)
    tests.gen_reads(100,[(0,50,75), (0, 85,110)])
    tests.write_assembly("./testcases/test_005.assembly.fasta")
    tests.write_reads("./testcases/test_005.reads.fasta")
    f = open("./testcases/test_005.oracle", "w")
    f.write(">1\n" + "0"*50 + "1"*25 + "0"*10 + "1"*25 + "0"*390 + "\n>2\n" + "0"*500 + "\n>3\n" + "0"*500 + "\n>4\n" + "0"*500)
    f.close()
