# CMSC737 - Assembly Model Testing #

## Goal ##
Design software to determine whether an assembly satisfies a set of constraints.

## Motivation ##
The genome sequence of an organism is a vital resource for biologists trying to better understand its function and evolution. Generating this sequence is not an easy task as modern sequencing technologies can only “read” small pieces of the genome. These sequences, known as *reads*, have to be pieced together by tools called assemblers using a collection of different heuristics since in almost all practical cases, **assemblers** cannot fully and accurately reconstruct the genome.

It is a very difficult job to evaluate the correctness of an assembly, but there are a few constraints that should hold up in the majority of cases.  Students will be given the task of creating tools that determine whether an assembly satisfies a given set of constraints.

## Background ##
**READ FIRST!** http://www.cbcb.umd.edu/research/assembly_primer.shtml.  This will give you a better background than I ever could.  Below are a few terms that will be used frequently during this project.  Please notify me if you have any questions about the terms.

### Sequence/read ###
A single DNA sequence produced from some experiment. I will use sequence and read interchangeably.
http://en.wikipedia.org/wiki/DNA_sequencing

### FASTA ###
A flat file to store DNA sequences in the format of “>header [newline] dna sequence”.  The DNA sequences are usually split every _X_ characters for readability purposes.  Each _>_ represents the start of a new record.  
*The majority of your data will be in this format!*
```
>header_name
ATCGTCAT
AGGATACA
>second_header
TTTCATTCC
```
http://en.wikipedia.org/wiki/FASTA_format

### Mate-pair ###
In most sequencing projects, the sizes of the fragments generated through the shotgun process are carefully controlled, thus providing a link between the sequence reads generated from the ends of a same fragment (called paired-ends or mate-pairs).  The *insert* size is the end-to-end distance between the reads ( *length of both reads + distance separating the reads* ). length is often known beforehand (but it is possible to figure out empirically).

### De novo assembly ###
Assembling the data by only looking at the reads without using any prior known information about the genome (opposite of referenced-based assembly).

### Contig ###
Contiguous pieces of DNA.  
http://en.wikipedia.org/wiki/Contig

### SAM (Sequence Alignment/Map) format ###
SAM format is a generic format for storing sequence alignments, e.g., from reads to assemblies/contigs/references/etc.

http://samtools.sourceforge.net/

http://samtools.sourceforge.net/SAMv1.pdf

 
## Constraints ##

### Group 1: Read coverage ###
Ideally, the sequencing process is uniform, producing reads uniformly at random from the underlying genome.  In other words, the number of times a basepair (bp) is covered by reads should be roughly the same across the assembly.  Regions of the assembly that have far deeper coverage than expected may be a repetitive sequence that has been compressed!

**Students must find regions of the assembly where the average coverage exceeds a given threshold.**

#### Input ####
* Assembly ( _FASTA format_ )
* Sequences ( _FASTA format_ )
* Window size - calculate the average coverage for that window of sequence.
* Standard deviations - cutoff stdev above the average to signal a mis-assembly.

#### Output ####
* Standard error:
 * Coverage statistics, window size.
* Standard out:
 * Genomic windows where the average coverage is above the threshold.

### Group 2: Mate-pair size agreement ###
Mate-pairs from a sequencing library should be a predetermined distance apart in the assembly.  If this value varies greatly in the actual assembly, it may be the sign of a potential misassembly (potentially due to collapsed/expanded repeats).

**Students must find regions of the assembly where the mate-pair size contraints are invalidated.**

#### Input ####
* Assembly ( _FASTA format_ )
* Sequences ( _FASTA format_ )
* Insert size ( _integer_ )
* Standard deviations - Standard
 
#### Output ####
* Reads that fail to align within the correct distance of each other and their corresponding genomic position.


## Strategies ##
For these projects, students will **not** have to worry about writing the code to aligning the reads.  This is done for you by a very popular (and created at Maryland) tool called **Bowtie2** (http://bowtie-bio.sourceforge.net/bowtie2/index.shtml).

The first thing ***everyone*** should do is complete the [Getting Started](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#getting-started-with-bowtie-2-lambda-phage-example) tutorial for Bowtie2.  This will teach you the basics of aligning sequences to a reference assembly and how to produce the SAM alignment file.

*These projects rely on using existing tools!*  There are FASTA parsers for every programming language ([BioPython](http://biopython.org/wiki/Main_Page), [BioRuby](http://www.bioruby.org/), [C++](http://www.seqan.de/), [Java](http://biojava.org/wiki/Main_Page), [R](http://www.bioconductor.org/)).  Similarly, there are a lot SAM parsers out there: [SAMtools](http://samtools.sourceforge.net/).

Below are few ideas to help you implement the test software.

### Group 1: Read coverage ###
* Run Bowtie2 using the sequences and assemblies to get the SAM file. 
* Parse the SAM file (using one of the parsers) to find where each sequence aligns on the assembly.
* Sort the alignments based on start position.
* Go through the assembly a window at a time, and count the number of times a read covers that window (or base).
* Print any windows that exceed the average coverage.

### Group 2: Mate-pair size agreement ###
* Run Bowtie2 using the sequences and assemblies (with mate-pair info) to get the SAM file.
* Parse the SAM file and print out the insert size of the alignment (hint: it's a field in the SAM file).
* If the insert size differs by a given number of standard deviation, print the reads. 

In order to get students started quickly, I will provide you with initial testcases (reads and assemblies).  Later in the project, students will need to construct their own testcases.

[AMOSValidate](http://sourceforge.net/apps/mediawiki/amos/index.php?title=Amosvalidate) is software that does similar constraint checking and can be a great resource.

### Simulating reads ###
*wgsim* is the tool I use to simulate reads. https://github.com/lh3/wgsim

Download it, and then run: ```gcc -g -O2 -Wall -o wgsim wgsim.c -lz -lm```

Next, you simply enter the reference fasta file you want to generate reads from:
```wgsim [options] <in.ref.fa> <out.read1.fq> <out.read2.fq>```

It produces mate-pair files, but you're fine only using one of the two files.  If I wanted to create 10 reads (each mate of length 100) without any error, I'd enter:
```wgsim -1 100 -2 100 -R 0.0 -X 0.0 -e 0.0 -N 10 influenza-output.fasta flu.1.fastq flu.2.fastq```

Notice how the output reads are in the fastq format instead of fasta.  Depending on the assembler, you may need to convert to fasta.  Fastq is similar to fasta but contains additional info about the quality of each basepair.  You can use a tool like this http://hannonlab.cshl.edu/fastx_toolkit/download.html to convert them to fasta.  I perfer just running a shell script like:
```awk 'NR % 4 == 1 || NR % 4 == 2' myfile.fastq | sed -e 's/@/>/' > myfile.fasta```

Below are read lengths typically produced by popular sequencing technologies.

| Technology     | Read length (avg) |
|----------------|-------------------|
| Illumina HiSeq | 100 bp            |
| 454            | 400 bp            |
| PacBio         | 1000 bp            |

### Generating assemblies ###
There are a collection of different assemblers students can use.  For a very detailed walkthrough, please check out the first part of the AMOS technical report (http://onlinelibrary.wiley.com/doi/10.1002/0471250953.bi1108s33/abstract) for instruction on the assembler Minimus.

Other popular assemblers include SGA (https://github.com/jts/sga), and SOAPdenovo (http://soap.genomics.org.cn/soapdenovo.html).

I recommend that first students generate reads from a ```true''' assembly.  Then manually introduce errors (creating breakpoints, duplicating segments, etc.) into the assembly.  This will provide a way for users to evaluate how well their framework detects the errors.

## Checkpoint 1
Due date: **November 12th**

By this date, each group should have a basic working implementation of their respective tool.  In addition, each group should have created and tested their tool on a collection of manually created test datasets.

Requirements:
* Working implementation with ```README``` file.  This ```README``` should describe how to use your tool and the output, specifically how you describe the misassemblies.
* Small collection of testcases uploaded to ```testcases/*/``` with a README file in each directory explaining the goal of the testcase.  Each testcase should contain a FASTA file of the reads (```input.fasta``` or ```input_1.fasta``` and ```input_2.fasta``` for the mate-pair group), a FASTA file for the assembly (```assembly.fasta```), and a file containing the known misassemblies that you will compare your tool's output with (```oracle```).  
* For now, include a ```run_test.sh``` script in each testcase directory that runs your tool and returns 0 if it finds all the misassemblies.

Submit a pull request with the above requirements: https://github.com/cmhill/assembly-testing

Currently, the ```run_test.sh``` in the root directory of the repository creates a jUnit XML file based on the testcase results.  It can be viewed here http://gandalf.cs.umd.edu:8080/job/Assembly%20testing/.  I'm currently working on a better plugin for viewing the testcase results.
