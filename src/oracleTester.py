def testOracle(outputFile, oracleFile):
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
        left = int(matchDataLine[0])
        right = int(matchDataLine[1])
        signal = matchDataLine[2]
        flag = 0
        count = 0
        for j in range(len(oracleLines)):
            dataLine = oracleLines[j].split('\t')
            if len(oracleLines[j]) == 0:
                continue
            oleft = int(dataLine[0])
            oright = oleft + int(dataLine[1])
            osignal = dataLine[2]
            if ((oleft >= left and right > oleft) or (oright >= left and oright < right)) and (osignal == signal):
                flag = 1
                flagArr[count] = 1
            count = count + 1
            
        if flag == 1:
            correct = correct + 1
        else:
            wrong = wrong + 1

    accuracyTestCases = float(correct)/(correct + wrong)
    accuracyDetection = float(sum(flagArr))/len(flagArr)
    print('Detection accuracy is ' + str(accuracyDetection))
    print('Accuracy among test cases is ' + str(accuracyTestCases))
    fileOutput.close()
            
