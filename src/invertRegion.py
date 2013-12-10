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

def repeatRegion(fastaLines, startPos1, endPos1, startPos2):
    linesToRepeat = fastaLines[startPos1:(endPos1+1)]
    linesToRepeat.reverse()

    for lineToRepeat in linesToRepeat:
        fastaLines.insert(startPos2, lineToRepeat)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="inputFastaFileName", type=str, help="fasta file name with content to be modified")
    parser.add_argument("-o", dest="outputFastaFileName", type=str, help="fasta file name with modified content")
    parser.add_argument("-s", dest="startPos", type=int, help="start position of where inversion starts")
    parser.add_argument("-e", dest="endPos", type=int, help="end position of where inversion ends")
    parser.add_argument("-r", dest="createRepeat", action="store_true", help="create a repeat following the original region and invert it.")

    args = parser.parse_args()
    assert(args.startPos <= args.endPos)

    with open(args.inputFastaFileName, "r") as f:
        lines = f.readlines()

    if args.createRepeat:
        repeatRegion(lines, args.startPos, args.endPos, args.endPos + 1)
        len = args.endPos - args.startPos
        args.startPos = args.endPos + 1
        args.endPos = args.startPos + len
    
    invertRegion(lines, args.startPos, args.endPos, args.endPos - args.startPos + 1)
    
    with open(args.outputFastaFileName, "w") as f:
        for line in lines:
            f.write(line)
    

