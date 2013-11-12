# CMSC737 - Mate-Pair Validation #

## Goal ##
Design software to determine whether an assembly satisfies a set of mate-pair constraints.

## Dependencies ##
We have dependencies on following tools/packages:

* python 2.7
* numpy
* biopython
* samtools
* pysam

## Usage ##
Below is the template of main usage of our tool. This time it only executes good-minus-bad analysis; however, it will execute rest of the analysis soon.
```
usage: matePairAnalysis.py [-h] --fasta FASTAFILENAME -1 READFILE1 -2
                           READFILE2 [--gmb BAMFILENAME]

Software to find misassemblies by doing mate-pair analysis

optional arguments:
  -h, --help            show this help message and exit
  --fasta FASTAFILENAME
                        fasta file name holding genome reference sequences
  -1 READFILE1          first part of the mate-pair reads
  -2 READFILE2          second part of the mate-pair reads
  --gmb BAMFILENAME     if present, do good minus bad analysis. this should be
                        a sorted and indexed BAM file.
```

## C/E Statistic ##
Running the ceStatistic:

'python ceStatistic.py [input.sam] [output]'

input.sam is the output of the bowtie2 aligner
output is the file to which the score are written

### C/E Statistic Test Cases ###
Each test case is available in a unique directory in the /testcases directory. Each test case can be run by the run_test.sh script in the directory

Since the CE Statistic is so highly sensitive to user input, they have been considered with somewhat arbitrary parameters. The test cases look to see that the inserted error was found within a region equal to (c*|error length|, where c is user configured) of the error. Errors are defined to be Z values with greater magnitude than 1.5 

### C/E Statistic Test Description ###

tc_ce_insertion: this test case only has insertions, it is designed to verify that the ceStatistic is correctly finding insertion errors. 

tc_ce_deletion: this test case has only deletions, it is designed to verify that the ceStatistic is correctly finding deletion errors. 





## Gaussian Constraint ##
### Algorithm ###
The algorithm is is as follows:
1) Given the reads, align the reads with the assembled genome using bowtie2
2) Once alignment has been made, compute the global mean and the standard deviation
3) Depending on the distance between paired ends in the sam file, the global mean and standard deviation, mark the region in the asssembly as potentially incorrect

### Usage ###

Since, the Gaussian Constraint is one of the many algorithms we are trying to find mis-assemblies, we have a python file which marks segment in the genome and it takes 3 arguments, the location of the sam file, the location of the output file where you want to write the regions of the mis-assembly and the read read length of the assembly, the function call is as follows:

gCk(samLocation, writeLocation, readLength)

The function can be imported as a python module and used as needed.

We also provide a tool (genAsblyAndOrcl.py) to generate automated test cases in the form of a python script. It creates a genome sequence and mutates it by adding and deleting fragments from the original sequence and then marks the position of the inserts and deletes which is used as oracle information

### Test Case Description ###

In the first test case (tc_gau_ins), we generate a random sequence of length 100000 and mutate it at several positions
 by deleting random sequences. We generate reads from the original sequence and align the reads with
 the mutated sequence using bowtie. Finally, we use the Gaussian hypothesis to mark valid regions in
 the genome. The oracle information is stored in 'output.txt' and the bad regions by the tool are 
stored in 'match.txt', results obtained by comparing 'match.txt' and 'output.txt' are stored in 'result.txt'

In the second test case (tc_gau_del) deletions are made in the genome sequence

In the third test case (tc_gau_ins_del) insertions and deletions both are made in the genome sequence

In all test cases, the genome size is 100000, read length is 40 and distance between paired ends is 200.

It takes a couple of seconds for the gaussian constraint to run for a genome sequence of size 100000 on a 1.3Ghz processor

The results of alignment are stored in match.txt and the score computed between the output of our tool with the oracle is written in result.txt

## Good-Minus-Bad Analysis ##
### Algorithm ###
The generic algorithm is as follows:

1. Classify mate-pair reads as bad and good pairs
2. Find the bad and good mate-pair reads covering a specific base-pair
3. Compute score for that base pair
4. Draw the score curve as a function of base pairs
5. Low scored regions are indicators of misassembly

This generic algorithm contains vague statements. We fill the gaps in these statements by following heuristics and definition in Kim et al. [1]. First, we should define what it takes to be a bad or good mate-pair. We took two times the average mate-pair insert size as our threshold value. If mate-pair insert size above this threshold, we mark it as bad. Other mate-pairs marked as good.

Second, we determine a scoring fuction. Each base pair is scored by subtracting number of bad clones from number of good clones covering this specific base pair.

Finally, we take negative scored regions as low scored regions. That is, negative regions indicates misassembly.

### Usage ###
As mentioned in the beginning of this document, good-minus-bad analysis can be executed in following way:
```
usage: matePairAnalysis.py [-h] --fasta FASTAFILENAME -1 READFILE1 -2
                           READFILE2 [--gmb BAMFILENAME]

Software to find misassemblies by doing mate-pair analysis

optional arguments:
  -h, --help            show this help message and exit
  --fasta FASTAFILENAME
                        fasta file name holding genome reference sequences
  -1 READFILE1          first part of the mate-pair reads
  -2 READFILE2          second part of the mate-pair reads
  --gmb BAMFILENAME     if present, do good minus bad analysis. this should be
                        a sorted and indexed BAM file.
```

### Test cases ###
We use "lambda virus" genome in this test. The reference genome and reads used in this test is taken from Bowtie 2 tutorial. We created BAM file and its index by using combination of Bowtie 2 and samtools.

We pick this test for our feasibility study. The fasta file for the genome contains only single reference and we created an artificial misassembly on the genome by inverting region(s) between base pair locations listed in the respective oracle file. 

In the first test (tc_gmb_1), we do inversion on single long region (compared to tc_gmb_2), 2100 base pairs. Inverting only one region simplifies the test and doing inversion on a long region should increase chances for misassembly region detection. Both these properties are ideal for a starter feasibility test.

In the second test (tc_gmb_2), we do inversion on single long region (compared to tc_gmb_1), 700 base pairs. Doing inversion on shorter region tests the sensitivity of our analysis to the length of the region.

In the third test (tc_gmb_3), we do inversion on multiple regions; more specifically, 3 regions. In other feasibility good-minus-bad analysis test cases (tc_gmb_1 and tc_gmb_2), we tested on a single region. By inverting multiple regions, we test whether having more than one inversion have negative effect on our analysis.

## Output Format ##
We are considering to output 4 tab-seperated columns. First column will be the name of the reference where the misassembly occured. Second and third column will refer to leftmost and rightmost base pair locations, respectively. Finally, fourth column refers to type of the misassembly in this region. An example output would look like below:
```
gi|9626243|ref|NC_001416.1|     19950   20650   inversion
gi|9626243|ref|NC_001416.1|     29960   30310   inversion
gi|9626243|ref|NC_001416.1|     45010   45430   inversion
```

We picked this format since it will allow us to easily merge misassembly regions from our different analysis tools. However, we are still thinking over adding new columns that might help us attribute confidence measures to misassembly regions.

## References ##
1. Sun Kim, Li Liao, Michael P. Perry Shiping Zhang and Jean-Francois Tomb. A computational approach to sequence assembly validation