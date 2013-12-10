




python ../../breakpoint-detection/generate_unaligned.py   ../../data/influenza-A/influenza-A.assembly.fasta ../../data/influenza-A/influenza-A.sequences.fasta influenzaUnaligned.txt


#attempt to align 
python ../../breakpoint-detection/breakpoint_indices.py -a  ../../data/influenza-A/influenza-A.assembly.fasta -u influenzaUnaligned.txt -o errorDetected.txt --alpha 8 --algorithm naive

#rm -f influenzaUnaligned.txt
rm -f *.sam


exit 0
