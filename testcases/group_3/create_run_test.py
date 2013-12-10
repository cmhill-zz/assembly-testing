import sys

if len(sys.argv) != 8:
	print 'provide input and output files and numbers'
	sys.exit()

input = open(sys.argv[1],'r')

raw = input.read()

input.close()

num1 = sys.argv[3]
num2 = sys.argv[4]
num3 = sys.argv[5]
num4 = sys.argv[6]
num5 = sys.argv[7]


output = open(sys.argv[2],'w')
raw = raw.replace('<1>',num1)
raw = raw.replace('<2>',num2)
raw = raw.replace('<3>',num3)
raw = raw.replace('<4>',num4)
raw = raw.replace('<5>',num5)

output.write(raw)
output.close()
