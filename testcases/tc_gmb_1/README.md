We use "lambda virus" genome in this test. The reference genome and reads used in this test is taken from Bowtie 2 tutorial. We created BAM file and its index by using combination of Bowtie 2 and samtools.

We pick this test for our feasibility study. The fasta file for the genome contains only single reference and we created an artificial misassembly on the genome by inverting region between base pair locations listed in oracle file. In this test we do inversion on single long region (compared to tc_gmb_2), 2100 base pairs.

Inverting only one region simplifies the test and doing inversion on a long region should increase chances for misassembly region detection. Both these properties are ideal for a starter feasibility test.