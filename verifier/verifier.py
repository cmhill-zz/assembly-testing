import random
import sys
from optparse import OptionParser
import math

      
def main():
    parser = OptionParser()
    parser.add_option('-o',"--oracle-file",dest="oracle_file")
    parser.add_option("-r","--result-file", dest = "result_file")

    (options, args) = parser.parse_args()

    if not options.oracle_file:
        print 'provide oracle file -o'
        sys.exit()
    if not options.result_file:
        print 'provide result file -r'
        sys.exit()

    in_oracle = open(options.oracle_file,'r')
    errors = []

    for line in in_oracle:
        tokens = line.split()
        contigName = tokens[0]
        errorStart = int(tokens[1])
        errorEnd = int(tokens[2])

        errors.append((errorStart,errorEnd))

    in_oracle.close()

    #have tuples in errors

    predictions = []

    in_predictions = open(options.result_file,'r')
    for line in in_predictions:
        tokens = line.split()
        contigName = tokens[0]
        errorStart = int(tokens[1])
        errorEnd = int(tokens[2])

        predictions.append((errorStart,errorEnd))

    in_predictions.close()


    #have errors, predictions

    foundErrors = 0
    totalErrors = len(errors)

    if totalErrors == 0:
        print 'There were zero errors to find.'
        sys.exit()

    #check: for each error, is there a predicted error which is within 10 base pairs
    for (errorStart,errorEnd) in errors:
        foundError = False
        for (predictionStart,predictionEnd) in predictions:
            if math.fabs(predictionStart-errorStart) < 50:
                foundError = True
                break

        if foundError == True:
            foundErrors+=1


    if float(float(foundErrors)/float(totalErrors)) > .2:
        print 'Found more than 20 percent of the errors!'
    else:
        print 'Failed to find more than 20 percent of the errors.'


if __name__ == '__main__':
    main()