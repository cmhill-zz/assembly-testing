python ../../src/matePairAnalysis.py --fasta delTest.fasta -1 r1.fq -2 r2.fq --gau
rm *.sam *.bam
python eval_gau_del.py