# BNGP
For the BNGP course, a pipeline has been developed. The pipeline consists of a combination of self-written scripts and existing applications that come together
in an automated Snakemake file. The pipeline consists of several parts/rules, each of which is briefly explained below.

To start, the pipeline is called using the following command:
snakemake --cores 4 --snakefile snakefile_s1125091 all

The first time the pipeline is run, all rules will be executed starting with the all rule. The all rule contains all the output files that need to be generated
by the pipeline. In the next rule, l.clavipes_genoom, the genome of l.clavipes is retrieved to be used further in the pipeline. Now the inventory process can
begin in the inventory rule. The inventory.py script is run here, which provides an inventory of how many reads the files contain, the average read length,
the minimum read length, the maximum read length, average GC percentage, and finally, the average GC percentage at each position. This information is saved 
in the files inventory_file1 and inventory_file2. Now, the reads can be trimmed in two files. Since they are paired reads, if one read is removed, the paired
read in the other file should also be removed. The script uses the sliding window method to determine the phred scores of the nucleotides. A window size of 3
was chosen (often, a default window of 4 is used) because it is not about very long reads. A higher window would also result in a higher average phred score,
while there may still be poor nucleotides with low phred scores within the window that would be overlooked. The nucleotides that fall within the window must
each have an average phred score greater than the cutoff of 35 to include the first nucleotide of the window and not trim it. An average phred score of 30 was
chosen because the phred scores at the beginning and end of the read are often quite low and should not be included. With an average phred score of 35, there
is a 99.95% chance that the base has been called correctly. Finally, the remaining sequence must be longer than 30 nucleotides to avoid being removed.
The obtained trimmed reads are saved in the files bngsa_mietinfected_1_trimmed.fastq and bngsa_mietinfected_2_trimmed.fastq. Next, in the next rule, inventory_trim,
another inventory is performed, this time on the two files with trimmed reads.

Now, the alignment rule can begin. In this rule, the genome of L.clavipes is first indexed using the Bowtie application. Alignment then takes place between two files
and the genome. The results of this are saved in a SAM file called SAMPLE.s. In the next rule, sam_bsm, the SAM file is converted to another format. Using samtools,
the SAM file is converted to a BAM file to save storage space and BAM files are faster to manipulate. Furthermore, the BAM file is also sorted. Next, with the sorted
BAM file, the insertions, deletions, and SNPs are determined. This is done using the tool bcftools mpileup. The results of this are saved in both a zipped vcf file and
an unzipped vcf file. Then, the consensus rule is called, which indexes the zipped vcf file and then determines the consensus that is saved in the file
consensus_output.fa. Finally, the investigation rule is called. In this rule, the number of insertions, deletions, and SNPs are determined. The number of all possible
mutation combinations is also displayed.
