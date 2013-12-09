f = open('oracle.txt', 'r')
out = open('oracle', 'w')

for lines in f:
    data = lines.split('\t')
    contig = data[0]
    left = int(data[1])
    right = int(data[2]) + left
    error = data[3]
    out.write(contig + '\t' + str(left) + '\t' + str(right) + '\t' + error)

out.close()
f.close()
