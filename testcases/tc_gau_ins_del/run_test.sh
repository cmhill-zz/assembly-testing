python ../../src/matePairAnalysis.py --fasta insDelTest.fasta -1 r1.fq -2 r2.fq --gau
rm *.sam *.bam
python eval_gau_ins_del.py