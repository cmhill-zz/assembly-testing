#!/usr/bin/python

def invertRegion(fastaLines, startPos, endPos, invLen):
    count = 0
    if startPos <= 0:
        lines = fastaLines[endPos::-1]
    else:
        lines = fastaLines[endPos:(startPos-1):-1]

    invStart = ((endPos - startPos + 1) - invLen) / 2
    for line in lines:
        if count >= invStart and count < (invStart + invLen):
            line = line.strip()[::-1] + '\n'
        fastaLines[startPos + count] = line
        count = count + 1

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="inputFastaFileName", type=str, help="fasta file name with content to be modified")
    parser.add_argument("-o", dest="outputFastaFileName", type=str, help="fasta file name with modified content")
    parser.add_argument("-s", dest="startPos", type=int, help="start position of where inversion starts")
    parser.add_argument("-e", dest="endPos", type=int, help="end position of where inversion ends")

    args = parser.parse_args()
    assert(args.startPos <= args.endPos)

    with open(args.inputFastaFileName, "r") as f:
        lines = f.readlines()

    invertRegion(lines, args.startPos, args.endPos, args.endPos - args.startPos + 1)
    
    with open(args.outputFastaFileName, "w") as f:
        for line in lines:
            f.write(line)
    

