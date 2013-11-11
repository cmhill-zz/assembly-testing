"""
Input: an assembly fasta file and a set of unaligned reads in fasta format.
Input: alpha, window size at the beginning of the unaligned reads.
Output: a distribution over the indices of the assembly where errors are likely

Example usage (from inside tutorials directory):
python breakpoint_indices.py -a ../../data/influenza-A/influenza-A.assembly.fasta -u unaligned.txt --alpha 5
"""

import sys
from optparse import OptionParser


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
			indices.append(resultIndex)
			currentStart=resultIndex+1

	return indices

# given a list of singletons, an assembly, and a windowsize alpha
# returns an array where each index represents the number of singletons that match at that point
# with that alpha
def naiveBreakpointDetect(singletons,assembly,alpha):
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

	return matchArray




def Main():
	parser = OptionParser()
	parser.add_option("-a","--assembly-file", dest = "assembly_file")
	parser.add_option("-u","--unaligned-file",dest = "unaligned_file")
	parser.add_option("--alpha",dest = "alpha")

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

	alpha = int(options.alpha)

	print 'Using alpha of: '+str(alpha)

	#read assembly
	assemblyString = readAssembly(options.assembly_file)

	print 'Successfully read assembly of length %d' % len(assemblyString)

	#read singletons
	singletons = readSingletons(options.unaligned_file)

	print 'Successfully read %d singletons' % len(singletons)

	#match singletons to assembly
	matchArray = naiveBreakpointDetect(singletons,assemblyString,alpha)



if __name__=="__main__":
	Main()