def testOracle(outputFile, oracleFile, resultFile):
    fileOutput = open(outputFile)
    matchData = fileOutput.read()
    matchData = matchData.split('\n')
    fileOracle = open(oracleFile)
    dataOracle = fileOracle.read()
    oracleLines = dataOracle.split('\n')
    fileOracle.close()
    correct = 0
    wrong = 0
    flagArr = [0] * (len(oracleLines) - 1)
    for i in range(len(matchData)):
        matchDataLine = matchData[i].split('\t')
        if len(matchData[i]) == 0:
            continue
        contig = matchDataLine[0]
        left = int(matchDataLine[1])
        right = int(matchDataLine[2])
        signal = matchDataLine[3]
        flag = 0
        count = 0
        for j in range(len(oracleLines)):
            dataLine = oracleLines[j].split('\t')
            if len(oracleLines[j]) == 0:
                continue
            ocontig = dataLine[0]
            oleft = int(dataLine[1])
            oright = int(dataLine[2])
            osignal = dataLine[3]
            if ((oleft >= left and right > oleft) or (oright >= left and oright < right)) and (osignal == signal) and (ocontig == contig):
                flag = 1
                flagArr[count] = 1
            count = count + 1
            
        if flag == 1:
            correct = correct + 1
        else:
            wrong = wrong + 1

    accuracyTestCases = float(correct)/(correct + wrong)
    accuracyDetection = float(sum(flagArr))/len(flagArr)

    f = open(resultFile, 'w')
#    print('Detection accuracy is (how many of the locations detected are actually errors) ' + str(accuracyDetection) + '\n')
#    print('Accuracy among test cases is (how may errors introduced were covered) ' + str(accuracyTestCases) + '\n')
    f.write('Detection accuracy is (how many of the locations detected are actually errors) ' + str(accuracyDetection) + '\n')
    f.write('Accuracy among test cases is (how may errors introduced were covered) ' + str(accuracyTestCases) + '\n')
    f.close()

    fileOutput.close()
