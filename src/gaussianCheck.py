#This file reads a sam file, computes the global mean and standard deviation between the mate pairs
#and then uses this information to figure out which poritions of the assembly are potentially bad
#and then writes the potentially bad locations and the conflicting reads to a file

import os
import math

def gCk(samLocation, writeLocation, readLength):

    inputFile = open(samLocation, 'r');

    tmp = inputFile.readline();
    tmp = inputFile.readline();
    tmp = inputFile.readline();

    matePairDistanceSum = 0;
    matePairLengthArray = [];

    numValidPoints = 0;

    for lines in inputFile:
        data = lines.split('\t');
        length = math.fabs(int(data[8]));
        signLength = int(data[8])
        #do not count pairs which are not found and those which are too out of place
        #we know that insert length cannot be greater than 1000
        if signLength > 0 and signLength < 500:
            matePairDistanceSum = matePairDistanceSum + length;
            matePairLengthArray.append(length);
            numValidPoints = numValidPoints + 1;
 
    meanDistance = float(matePairDistanceSum)/(numValidPoints);

#    print(numValidPoints)

    variance = 0;

    for distance in matePairLengthArray:
        variance = variance + (distance - meanDistance)*(distance - meanDistance);

    variance = float(variance)/(numValidPoints);
    standardDeviation = math.sqrt(variance);
#    print(meanDistance);
#    print(standardDeviation);

    inputFile.close();

    #start processing again to mark locations which are bad
    inputFile = open(samLocation, 'r');

    tmp = inputFile.readline();
    tmp = inputFile.readline();
    tmp = inputFile.readline();

    minLength = meanDistance - standardDeviation;
    maxLength = meanDistance + standardDeviation;

    count = 0
    badInsertInterval = [];
    badDeleteInterval = [];

    for lines in inputFile:
        data = lines.split('\t');
        signLength = int(data[8]);
        length = math.fabs(int(data[8]));
        location = int(data[7]);
        readCount = data[0];

        #if location value is 0 it means that mate pair was not matched, continue
        if location == 0:
            count = count + 1;
            continue;
        
        #now we only need to check for mate pairs whose distance is greater than zero
        if signLength > 0 and (length < minLength or length > maxLength):
            if length > meanDistance:
                badInsertInterval.append([location - length + readLength, location])
            else:
                badDeleteInterval.append([location - length + readLength, location])
        count = count + 1;

    inputFile.close();
    out = open(writeLocation, 'w')

    if (len(badDeleteInterval) > 0):
        badDeleteInterval = merge(badDeleteInterval)

    if (len(badInsertInterval) > 0):
        badInsertInterval = merge(badInsertInterval)

    print('Start of artificial test case, gaussian constraint')
    print('\n')

    for intervals in badDeleteInterval:
        out.write(str(int(intervals[0])) + '\t' + str(int(intervals[1])) + '\td\n')
        print('1\t' + str(int(intervals[0])) + '\t' + str(int(intervals[1])) + '\tdeletion, found by mate pair\tNIL')
    for intervals in badInsertInterval:
        out.write(str(int(intervals[0])) + '\t' + str(int(intervals[1])) + '\ti\n')
        print('1\t' + str(int(intervals[0])) + '\t' + str(int(intervals[1])) + '\tinsertion, found by mate pair\tNIL')

    print('End of test case')
    print('\n')

    out.close()

def sortList(l, sort = True):
    if sort:
        sl = sorted(tuple(sorted(i)) for i in l)
    else:
        sl = l
    if len(sl) > 1:
        if sl[0][1] >= sl[1][0]:
            sl[0] = (sl[0][0], sl[1][1])
            del sl[1]
            if len(sl) < len(l):
                return sortList(sl, False)
    return sl

def merge(times):
    times = sortList(times)
    saved = list(times[0])
    for st, en in sorted([sorted(t) for t in times]):
        if st <= saved[1]:
            saved[1] = max(saved[1], en)
        else:
            yield tuple(saved)
            saved[0] = st
            saved[1] = en
    yield tuple(saved)
