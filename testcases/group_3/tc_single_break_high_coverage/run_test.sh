#Generate assembly on short original with one error (2000 out of 3000)
python ../../../errorgenerator/errorGen.py -a ../../../data/buchnera/3000/buchnera-udp.assembly.fasta -o assembly.fasta -m oracle -e 2000 -l 200

#Generate 5x read coverage over error assembly
wgsim -1 300 -2 300 -R 0.0 -X 0.0 -e 0.0 -N 100 assembly.fasta reads.1.fastq reads.2.fastq

#Convert fastq to fasta
python ../../../errorgenerator/convertFASTQ.py reads.1.fastq reads.fasta

rm -f reads.1.fastq 
rm -f reads.2.fastq


python ../../../breakpoint-detection/generate_unaligned.py  ../../../data/buchnera/3000/buchnera-udp.assembly.fasta reads.fasta singleUnaligned.txt


#attempt to align 
python ../../../breakpoint-detection/breakpoint_indices.py -a ../../../data/buchnera/3000/buchnera-udp.assembly.fasta -u singleUnaligned.txt -o errorDetected.txt --alpha 20 --algorithm naive

#run verifier
python ../../../verifier/verifier.py -o oracle -r errorDetected.txt

rm -f singleUnaligned.txt
rm -f singleErrorAssembly.fasta
rm -f singleReads.1.fasta
rm -f *.sam

exit 0