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

### C/E Statistic Usage ###
'python ceStatistic.py <input.sam> <output>'

input.sam is the output of the bowtie2 aligner
output is the file to which the score are written

### C/E Statistic Test Cases ###
Each test case is available in a unique directory in the /testcases directory.
Each test case can be run by the run_test.sh script in the directory

Since the CE Statistic is so highly sensitive to user input, they have been considered with somewhat arbitrary parameters. 
The test cases look to see that the inserted error was found within a region equal to (c*|error length|, where c is user configured) of the error. 
Errors are defined to be Z values with greater magnitude than 1.5 

### C/E Statistic Test Description ###

tc_ce_insertion: this test case only has insertions, it is designed to verify that the ceStatistic is correctly finding insertion errors. 

tc_ce_deletion: this test case has only deletions, it is designed to verify that the ceStatistic is correctly finding deletion errors. 





## Gaussian Constraint ##
**_TODO:_**

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