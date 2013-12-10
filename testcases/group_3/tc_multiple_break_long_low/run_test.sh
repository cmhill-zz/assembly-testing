rm -f errorDetected.txt
rm -f success

#Generate assembly on short original with one error (2000 out of 3000)
python ../../../errorgenerator/errorGen.py -a ../../../data/buchnera/600000/buchnera-udp.assembly.fasta -o assembly.fasta -m oracle -e 5000 -l 200

#Generate 5x read coverage over error assembly
wgsim -1 600 -2 600 -R 0.0 -X 0.0 -e 0.0 -N 1000 assembly.fasta reads.1.fastq reads.2.fastq

#Convert fastq to fasta
python ../../../errorgenerator/convertFASTQ.py reads.1.fastq reads.fasta

rm -f reads.1.fastq 
rm -f reads.2.fastq


python ../../../breakpoint-detection/generate_unaligned.py  ../../../data/buchnera/600000/buchnera-udp.assembly.fasta reads.fasta singleUnaligned.txt


#attempt to align 
python ../../../breakpoint-detection/breakpoint_indices.py -a ../../../data/buchnera/600000/buchnera-udp.assembly.fasta -u singleUnaligned.txt -o errorDetected.txt --alpha 20 --algorithm naive


if [ ! -f "errorDetected.txt" ]
then
    echo "No errors found"
    exit 1
fi

#run verifier
python ../../../verifier/verifier.py -o oracle -r errorDetected.txt


if [ ! -f "success" ]
then
    echo "No errors found"
    exit 1
fi

rm -f singleUnaligned.txt
rm -f singleErrorAssembly.fasta
rm -f singleReads.1.fasta
rm -f *.sam

exit 0
