import random
from optparse import OptionParser

class AssemblyMesser(object):
    """docstring for AssemblyMesser"""
    def __init__(self, options):
        super(AssemblyMesser, self).__init__()
        self.options = options
        self.header = ""
        self.errorPoints = []
        self.bad_data = ""
        
    def setHeader(self,header):
        """docstring for setHeader"""
        self.header = header
    
    def getHeader(self):
        """docstring for getHeader"""
        return self.header
    
    def setErrorPoints(self, ep):
        self.errorPoints = ep
        
    def getErrorPoints(self):
        return self.errorPoints
    
    def setBadData(self, bd):
        self.bad_data = bd
    
    def getBadData(self):
        return self.bad_data
    
        

def errorWrite(messer):
    options = messer.options
    with open (options.output_file, "w") as outputFile:
    	outputFile.write(messer.getHeader()+"\n")
    	outputFile.write(messer.getBadData()+"\n")

    with open (options.metadata_file, "w") as metaDataFile:
    	metaDataFile.write(str(messer.getErrorPoints()))		
    

def errorDo(messer):
    
    opts = messer.options
    with open(opts.assembly_file,"r") as assembly:
        good_data = assembly.read().replace('\n','')
    messer.setHeader(good_data[:good_data.index('cds')+3])
    
    genomeString = good_data[good_data.index('cds')+3:]
    
    errorStartPoints = []
    
    start = 0
    errorLength = opts.error_length
    #Errors : 
    # 1. Inversion
    # 2. Rearrangement
    # 3. Insertion/Deletion

    for iter in range(0,(len(genomeString)/opts.error_frequency)):
    	if (iter*opts.error_frequency < len(good_data)):
    		errorStartPoints.append(random.randint(start, (iter+1)*opts.error_frequency))
    		start += opts.error_frequency
    	else:
    		errorStartPoints.append(random.randint(start, len(data)))


    invertedString = genomeString
    for i in errorStartPoints:
    	errorCode = 1
    	if (errorCode == 1):
            invertedString = invertedString[:i] + invertedString[i:i+errorLength][::-1] + invertedString[i+errorLength:]
    messer.setErrorPoints(errorStartPoints)
    messer.setBadData(invertedString)
            
    
def verifyOpts(options):
    if not options.assembly_file:
		print 'Provide assembly file (-a, --assembly-file)'
		sys.exit()
    
    if not options.output_file:
		print 'Provide output file (-o, --output-file)'
		sys.exit()
    
    if not options.metadata_file:
		print 'Provide metadata file (-m, --metadata-file)'
		sys.exit()
    
    if not options.error_frequency:
        options.error_frequency = 1000
    else:
        options.error_frequency = int(options.error_frequency)
        
    if not options.error_length:
        options.error_length = 20
    else:
        options.error_length = int(options.error_length)


def main():
    parser = OptionParser()
    parser.add_option("-a","--assembly-file", dest = "assembly_file")
    parser.add_option("-o","--output-file",dest = "output_file")
    parser.add_option("-m","--metadata-file",dest = "metadata_file")
    parser.add_option("-e","--error-frequency", dest = "error_frequency")
    parser.add_option("-l","--error-length", dest="error_length")
    
    (options, args) = parser.parse_args()
    
    verifyOpts(options)
    
    myMesser = AssemblyMesser(options)
    
    errorDo(myMesser)
    errorWrite(myMesser)
    
if __name__ == '__main__':
    main()    
	
	