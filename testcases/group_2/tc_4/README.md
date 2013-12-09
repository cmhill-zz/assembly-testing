In this test case, we generate a random sequence of length 100000 and mutate it at several positions
 by deleting random sequences. We generate reads from the original sequence and align the reads with
 the mutated sequence using bowtie. Finally, we use the Gaussian hypothesis to mark valid regions in
 the genome. The oracle information is stored in 'output.txt' and the bad regions by the tool are 
stored in 'match.txt', results obtained by comparing 'match.txt' and 'output.txt' are stored in 'result.txt'