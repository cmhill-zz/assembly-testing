"""
Input: an assembly fasta file and a set of unaligned reads in fasta format.
Input: alpha, window size at the beginning of the unaligned reads.
Output: a distribution over the indices of the assembly where errors are likely

Example usage (from inside tutorials directory):
python breakpoint_indices.py -a ../../data/influenza-A/influenza-A.assembly.fasta -u unaligned.txt --alpha 5
"""

import sys
from optparse import OptionParser
from math import sqrt, pi, exp


#reads an assembly from a FASTA file as one contiguous string. Returns said string.
def readAssembly(assembly_file):
	infile = open(assembly_file,'r')

	assembly=[]
	headerCount = 0
	for line in infile:
		#if this line is a header line, skip it
		if line[0]==">":
			headerCount+=1
			continue
		else:
			assembly.append(line)


	print 'Read %d headers' % headerCount
	
	assemblyString = "".join(assembly)
	strippedString = assemblyString.strip().replace('\n','')
	return strippedString

#reads in a list of singletons from a FASTA file. Returns list of strings.
def readSingletons(unaligned_file):
	infile = open(unaligned_file,'r')

	singletons=[]
	currentSingleton=[]
	singletonCount=0
	for line in infile:
		if line[0]==">":
			singletonCount+=1
			
			#if the current singleton is not the empty list, join it and add it to the singletons list
			if len(currentSingleton)!=0:
				singletonString = "".join(currentSingleton)
				strippedString = singletonString.strip().replace('\n','')
				singletons.append(strippedString)
			
			currentSingleton=[]
			continue
		else:
			currentSingleton.append(line)

	#get last singleton, since there are no more header lines
	singletonString = "".join(currentSingleton)
	strippedString = singletonString.strip().replace('\n','')
	singletons.append(strippedString)

	return singletons


# given a singleton, an assembly, and a windowsize alpha
# returns a list of indices where the singleton matches the assembly

def matchSingleton(singleton,assembly,alpha):
	#ensure alpha is a small window
	if alpha >= len(singleton):
		print 'Alpha = '+str(alpha)+' is greater than length of singleton '+singleton
		sys.exit()
	
	#get alpha string
	alphaString = singleton[0:alpha]

	#result set of indices
	indices=[]

	resultIndex = 0
	currentStart=0
	while resultIndex != -1:
		resultIndex = assembly.find(alphaString,currentStart,len(assembly))
		if resultIndex != -1:
			print 'Found match at position: '+str(resultIndex)
			#now find where singleton stops matching assembly
			curInd = resultIndex
			for char in singleton:
				if char == assembly[curInd]:
					curInd+=1
					print 'matches up to %d' % curInd
				else:
					print 'distance: %d' % (curInd - resultIndex)
					break

			indices.append(curInd)
			currentStart=resultIndex+1

	return indices

# given a list of singletons, an assembly, and a windowsize alpha
# returns an array where each index represents the number of singletons that match at that point
# with that alpha
def naiveBreakpointDetect(singletons,assembly,alpha,outputFile=None):
	#initialize empty array
	matchArray = []
	for i in range(len(assembly)):
		matchArray.append(0)

	#for each singleton, increment matchArray everywhere a singleton matches
	i=1
	for s in singletons:
		print 'Processing singleton ' + str(i) + ' of ' + str(len(singletons))
		matchIndices = matchSingleton(s,assembly,alpha)
		for index in matchIndices:
			matchArray[index]+=1
		i+=1

	if outputFile != None:
		outputStream = open(outputFile,'w')

		
		errorCount = 0
		for i in range(len(matchArray)):
			if matchArray[i] > 0:
				outputStream.write("error_"+str(errorCount)+"\t"+str(i)+"\t"+str(i)+"\tbreak\t"+str(matchArray[i])+"\n")
				errorCount+=1

		outputStream.close()


	return matchArray

# generates a gaussian filter of size n with stdev 1
def gauss(n,sigma):
    r = range(-int(n/2),int(n/2)+1)
    return [1 / (sigma * sqrt(2*pi)) * exp(-float(x)**2/(2*sigma**2)) for x in r]

# given an array of numbers, an index at which to add the gaussian,
# the size of the window, and the stdev of the gaussian
# returns the array with the gaussian added
def addGaussian(arr,index,n,sigma):
	gaussian = gauss(n,sigma)
	startInd = index - (int(n/2))
	endInd = index + (int(n/2))

	gaussianCenter = int(n/2)

	for i in range(gaussianCenter):
		distance = gaussianCenter - i
		arrayIndex = index-distance
		if arrayIndex > 0 and arrayIndex < len(arr):
			arr[arrayIndex]+=gaussian[i]

	for i in range(gaussianCenter,len(gaussian)):
		distance = gaussianCenter - i
		arrayIndex = index-distance
		if arrayIndex > 0 and arrayIndex < len(arr):
			arr[arrayIndex]+=gaussian[i]		

	return arr


# given a list of singletons, an assembly, and a windowsize alpha
# returns an array where each index represents the number of singletons that match at that point
# with that alpha
def gaussianBreakpointDetect(singletons,assembly,alpha,n,sigma,outputFile=None):
	try:
		n = int(n)
	except:
		print 'n was: '+str(n)
		raw_input()
		sys.exit()

	#initialize empty array
	matchArray = []
	for i in range(len(assembly)):
		matchArray.append(0)

	#for each singleton, increment matchArray everywhere a singleton matches
	i=1
	for s in singletons:
		print 'Processing singleton ' + str(i) + ' of ' + str(len(singletons))
		matchIndices = matchSingleton(s,assembly,alpha)
		for index in matchIndices:
			addGaussian(matchArray,index,n,sigma)
		i+=1

	if outputFile != None:
		outputStream = open(outputFile,'w')

		outputStream.write("ContigName\tStartError\tEndError\ttype\tconfidence\n")
		
		errorCount = 0
		for i in range(len(matchArray)):
			if matchArray[i] > 0:
				outputStream.write("error_"+str(errorCount)+"\t"+str(i)+"\t"+str(i)+"\tbreak\t"+str(matchArray[i])+"\n")
				errorCount+=1

		outputStream.close()


	return matchArray




def Main():
	parser = OptionParser()
	parser.add_option("--algorithm",dest = "algorithm")
	parser.add_option("-a","--assembly-file", dest = "assembly_file")
	parser.add_option("-u","--unaligned-file",dest = "unaligned_file")
	parser.add_option("--alpha",dest = "alpha")
	parser.add_option("-o","--output-file",dest = "output_file")
	parser.add_option("--gauss-window",dest = "gauss_window")
	parser.add_option("--sigma",dest = "sigma")

	(options, args) = parser.parse_args()

	if not options.assembly_file:
		print 'Provide assembly file (-a, --assembly-file)'
		sys.exit()

	if not options.unaligned_file:
		print 'Provide unaligned reads file (-u, --unaligned-file)'
		sys.exit()

	if not options.alpha:
		print 'Provide alpha (--alpha)'
		sys.exit()

	output_file=None
	if options.output_file:
		output_file=options.output_file

	alpha = int(options.alpha)

	print 'Using alpha of: '+str(alpha)

	#read assembly
	assemblyString = readAssembly(options.assembly_file)

	print 'Successfully read assembly of length %d' % len(assemblyString)

	#read singletons
	singletons = readSingletons(options.unaligned_file)

	print 'Successfully read %d singletons' % len(singletons)
	

	#match singletons to assembly
	if options.algorithm == "naive":
		matchArray = naiveBreakpointDetect(singletons,assemblyString,alpha,output_file)
	elif options.algorithm == "window":
		if not options.gauss_window:
			print 'Provide --gauss-window'
			sys.exit()
		if not options.sigma:
			print 'Provide --sigma'
			sys.exit()

		n = int(options.gauss_window)
		sigma = float(options.sigma)

		matchArray = gaussianBreakpointDetect(singletons,assemblyString,alpha,n,sigma,output_file)
	else:
		print '--algorithm must be naive or window'
		print options.algorithm
		sys.exit()



if __name__=="__main__":
	Main()
