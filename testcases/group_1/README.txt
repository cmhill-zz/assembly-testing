################
Testcase catalog
################

TESTCASE_ID	GENOME		CONTIG_ID	START_REPEAT_SEGMENT	END_REPEAT_SEGMENT	READ_LENGTH (WGSIM)	NUMBER_READS(WGSIM)

tc_1		INFLUENZA-A	1			500		1500				500		10000	
tc_2		INFLUENZA-A 	1			500		1500				500		10000	
				2			500		1500			
tc_3		INFLUENZA-A	2			200		250				500		10000
				3			100		400					

tc_4		INFLUENZA-A	1			500		1500				100		20000
tc_5		INFLUENZA-A	1			500		1500				100		20000
				2			500		1500
tc_6		INFLUENZA-A	2			200		250				100		20000
				3			100		400			
tc_7	AEROPYRUM_PERNIX_K1	1 			100000		200000				100		20000
				1			300000		400000			
				1			500000		600000
				1			700000		750000
				1			800000		820000
tc_8	AEROPYRUM_PERNIX_K1	1			100000		600000				100		20000
tc_9		INFLUENZA-A	1			500		1500				100		20000
tc_10		INFLUENZA-A	1			500		1500				100		20000
				2			500		1500	
tc_11		INFLUENZA-A	2			200		250				100		20000
				3			100		400			
tc_12 		E_COLI_K12	1			100000		200000				500		10000
				1			300000		400000
				1			500000		600000
				1			700000		750000
				1			800000		820000
tc_13 		E_COLI_K12	1			100000		600000				500		10000


#####################
Testcase descriptions
#####################

- tc_1 introduces repeats along a segment of size 1000bp.
- tc_2 expans upon tc_1 by introducing repeats along two contigs. We strive to make sure that our program detects repeats across contigs.
- tc_3 contains a very short contig of length 50bp. The goal is to make sure that the program detects short repeats. 
- tc_4 uses a drastically reduced read length for wgsim and examines the impact of that read length. A higher number of reads is also introduced.
- tc_5 has the same rationale as tc_4, but extrapolates it to two contigs.
- tc_6 generalizes both tc_4 and tc_5, by introducing very small repeats. That is, we generate very small but double the amount of reads, detect repeats along two contigs,
and examine results on very small repeats (50 bp and 300bp).
- tc_7 changes the genome that we test on. We now test on the Aeropyrum Pernix K1 genome, which consists of about 1.5Mbp. We introduce a huge repeat,
of size 1MBP, a read length of 100 and 20000 reads and examine the results.
- tc_8 continues testing on Aeropyrum Pernix K1, and introduces the largest repeat that we deal with up to that point, consisting of 500Kbp.
- tc_9, tc_10 and tc_11 revert back to Influenza-A. They modify test cases tc_1, tc_2 and tc_3 by repeating the same tests only this time
with a read length one-fifth as much and double the read count.
- tc_12 tests on The E-Coli K12 bacterium, consisting of approximately 4.7Mbp. It is the largest genome that we have tested on. Repeats of various
lengths are detected, including 100Kbp, 50Kbp and 20Kbp.
- tc_13 generalizes tc_12 by searching for a repeat of size 500Kbp.