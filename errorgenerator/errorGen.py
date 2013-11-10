import random
filePath= raw_input("Enter file :")
fileWritePath=raw_input("Enter write file :")
fileWriteMetaPath=raw_input("Enter metadata file :")

with open (filePath, "r") as myfile:
    data=myfile.read().replace('\n', '')

errorFreq = 1000
genomeString = data[data.index('cds')+3:]

print genomeString[0:7][::-1]
#Errors : 
# 1. Inversion
# 2. Rearrangement
# 3. Insertion/Deletion
errorStartPoints = []
start = 0
for iter in range(0,len(genomeString)/errorFreq):
	if (iter*errorFreq < len(data)):
		errorStartPoints.append(random.randint(start, (iter+1)*errorFreq))
		start += errorFreq
	else:
		errorStartPoints.append(random.randint(start, len(data)))


print errorStartPoints
# write start points into file
print len(genomeString)
errorLength = 20
invertedString = genomeString
for i in errorStartPoints:
	errorCode = 1
	if (errorCode == 1):
		print i
		print invertedString[i:i+errorLength]
		invertedString = invertedString[:i] + invertedString[i:i+errorLength][::-1] + invertedString[i+errorLength:]


with open (fileWritePath, "w") as myFile:
	myFile.write(data[:data.index('cds')+3])
	myFile.write(invertedString)

with open (fileWriteMetaPath, "w") as myFile1:
	myFile1.write(str(errorStartPoints))		

myFile.close()
myFile1.close()
	
	