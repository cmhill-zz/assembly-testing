import os
import random

def generateValidation(seqLoc, modSeqLoc, errorIndexLoc, insertFlag, deleteFlag):
    writeLocation = seqLoc
    writeLocationMod = modSeqLoc
    errorLocationIndexes = errorIndexLoc

    genomeLength = 100000;
    minDiff = 40;
    rangeDiff = 20;
    insertSpacing = 3000;
    deleteSpacing = 2600;
    id = '1';

    referenceString = generateString(genomeLength);

    outputFile = open(writeLocation, 'w');
    i = 0
    outputFile.write('>gi| Software Testing ' + id + '\n')
    while i < (len(referenceString) - 80):
        outputFile.write(referenceString[i:i+80])
        outputFile.write('\n')
        i = i + 80
    outputFile.close();

    #Now remove some portions of this string and make some insertions in this genome
    i = 0;
    generatedString = '';
    deletionIndices = [];
    deletionLengths = [];
    insertionIndices = [];
    insertionLengths = [];

    #save indices where deletions have been made and store the length of the deletions
    if deleteFlag:
        while i < genomeLength - deleteSpacing:
            generatedString = generatedString + referenceString[i:i+deleteSpacing];
            tlength = random.randint(minDiff, minDiff + rangeDiff);
            deletionIndices.append(len(generatedString));
            deletionLengths.append(tlength);
            i = i + tlength + deleteSpacing;
        generatedString = generatedString + referenceString[i:genomeLength];

    i = 0;

    #save the locations where inserts are made taking into account the
    #deletions (if they have been made)
    if insertFlag:
        if deleteFlag:
            deletedLength = len(generatedString);
            tmpString = '';
            while i < deletedLength - insertSpacing:
                tmpString = tmpString + generatedString[i:i+insertSpacing];
                tlength = random.randint(minDiff, minDiff + rangeDiff);
                insertionIndices.append(len(tmpString));
                insertionLengths.append(tlength);
                deletionIndices = updateDeleteIndices(deletionIndices, len(tmpString), tlength);
                tmpString = tmpString + generateString(tlength);
                i = i + insertSpacing;
            tmpString = tmpString + generatedString[i:deletedLength];
            generatedString = tmpString;
        else:
            while i < genomeLength - insertSpacing:
                generatedString = generatedString + referenceString[i:i+insertSpacing];
                tlength = random.randint(minDiff, minDiff + rangeDiff);
                insertionIndices.append(len(generatedString));
                insertionLengths.append(tlength);
                generatedString = generatedString + generateString(tlength);
                i = i + insertSpacing;
            generatedString = generatedString + referenceString[i:genomeLength];

    #write the indices where deletions and inserts have been made and
    #also the length of the deletes and inserts
    modifiedFile = open(writeLocationMod, 'w');
    i = 0
    modifiedFile.write('>gim|Software Testing ' + id + '\n')
    while i < (len(generatedString) - 80):
        modifiedFile.write(generatedString[i:i+80])
        modifiedFile.write('\n')
        i = i + 80
    modifiedFile.close();
    errorLocationsFile = open(errorLocationIndexes, 'w');

    for i in range(len(insertionIndices)):
        errorLocationsFile.write(str(insertionIndices[i]) + '\t' + str(insertionLengths[i]) + '\ti\n');

    for i in range(len(deletionIndices)):
        errorLocationsFile.write(str(deletionIndices[i]) + '\t' + str(deletionLengths[i]) + '\td\n');

    errorLocationsFile.close();
    errorLocationsFile.close();

#generates a string of specified length
def generateString(length):
    string = '';
    dictionary = ['A', 'T', 'G', 'C'];
    for i in range(length):
        string = string + dictionary[random.randint(0, 3)];
    return string;

#updates the delete indices if an insert is made on the left of where the delete is performed
def updateDeleteIndices(deletionIndices, insertIndex, insertLength):
    for i in range(len(deletionIndices)):
        if deletionIndices[i] > insertIndex:
            deletionIndices[i] = deletionIndices[i] + insertLength;
    return deletionIndices;
