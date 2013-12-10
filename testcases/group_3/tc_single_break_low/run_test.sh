#!/bin/bash

#Generate assembly on short original with one error (2000 out of 3000)
python ../../../errorgenerator/errorgen.py -a ../../../data/buchnera/3000/buchnera-udp.assembly.fasta -o singleErrorAssembly.fasta -m singleErrorMetadata.txt -e 2000 -l 200

#Generate 5x read coverage over error assembly
wgsim -1 300 -2 300 -R 0.0 -X 0.0 -e 0.0 -N 50 singleErrorAssembly.fasta single.1.fastq single.2.fastq

#Convert fastq to fasta
python ../../../errorgenerator/convertFASTQ.py single.1.fastq singleReads.1.fasta

rm -f single.1.fastq 
rm -f single.2.fastq

python ../../../breakpoint-detection/generate_unaligned.py  ../../../data/buchnera/3000/buchnera-udp.assembly.fasta singleReads.1.fasta singleUnaligned.txt


#attempt to align 
python ../../../breakpoint-detection/breakpoint_indices.py -a ../../../data/buchnera/3000/buchnera-udp.assembly.fasta -u singleUnaligned.txt -o errorDetected.txt --alpha 20 --algorithm naive

rm -f singleUnaligned.txt
rm -f singleErrorAssembly.fasta
rm -f singleReads.1.fasta
rm -f *.sam

exit 0