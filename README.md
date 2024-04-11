# sshicstuff: a project that analyzes fastq files generated by ssDNA Hi-C Capture developped by Piazza lab

## Dependencies  
It is recommended to use a virtual environment to install the dependencies. We suggest you to use the 
requirements.yml file to install a conda environment. You can do it as follows:

```conda env create -f requirements.yml```

Then, activate the environment:
    
```conda activate sshic```

As it is still in 'development mode', you have to install the package in the environment (not yet packaged), 
you will need to add the path to the package folder (**/sshicstuff/sshic/core**) in your ```conda.pth``` environment variable :

```conda develop <path_to_the_package_core_directory>```


## Description  
This project analyzes the sequencing data generated after the ssDNA HiC Capture
protocol. These project has not yet been packaged as a python package (it will be soon). 
It includes multiples independents scripts which are executed one after the 
other according to the main script ```pipeline.py```. 
This pipeline is actually a downstream analysis extension of existing HiC data analysis pipeline such as hicstuff 
(https://github.com/koszullab/hicstuff). You can use it as follows:

### 1. Upstream script : oligos_replacement

(author : Loqmen Anani, Piazza Lab)  

It generates a genome from the original genome and the new oligos designed in the ssDNA Hi-C Capture
protocol. The new genome is a copy of the original exepted for the oligos regions, the sequence is 
replaced by the oligos sequence. Then, it adds -at the end of the new genome built- 
a new artificial chromosome named ```chr_art```
which is a concatenation of the original sequence of the oligos with their flanking regions.

Also, the program creates a ```.bed``` file that contains the 
coordinates of the oligos in the new genome and in the artificial chromosome and indicates if
the sequence is a flanking region or the oligo itself.

#### Oligo file structure

This file has to contained at least 6 columns with the **precises** headers below:

| chr | start | end | orientation | type | name | sequence_original | sequence_modified |
|-----|-------|-----|-------------|------|------|-------------------|-------------------|

- In the```chr``` column, it has to be the name of the chromosome.
Technically, it has to be the first word after the chevron ">" of the
first line describing the chromomse in the fasta file.
For example, if the fasta file is like:
> '>chr5 (10 000 bp)  
AAATTTTetc.'

The ```chr``` column name MUST be ```chr5```. 
**It is the string before the first space.**
- In the ```start``` column, the position of the first nucleotide (included) of the oligo 
(the first nucleotide of the chromosome is the number 1)

- In the ```end``` column, the position of the last nucleotide (included) of the oligo

- In the ```orientation``` column, ```C``` for Crick and ```W``` for Watson

- In the ```type``` column, ```ss``` (ssDNA HiC oligos captured),
```ss_neg``` ssDNA negative control (ssDNA HiC oligos not captured),
```ds``` (dsDNA HiC oligos captured),
```ds_neg``` dsDNA negative control (dsDNA HiC oligos not captured)

- In the ```name``` column, write the name of the oligo, all names must be different

- In the ```sequence_original``` column, the original sequence of the oligo

- In the ```sequence_original``` column, the modified sequence of the oligo

The first oligo is the number 0.

### 2. Hicstuff

(author : Koszul lab)

With the new genome created, the user can run the hicstuff package and thus creates a `fragments_list.txt` :


| id | chrom | start_pos | end_pos | size | gc_content |
|----|-------|-----------|---------|------|------------|


and a contacts sparse matrix file :


| frag_A | frag_B | count |
|--------|--------|-------|
 
Please check the hicstuff documentation for the structure of those files https://github.com/koszullab/hicstuff#file-formats.



### 3. ssDNA - HiC pipeline data analysis

(author : Nicolas Mendiboure, Piazza Lab)


#### Notes : data tree structure

It is highly recommended to have the following data tree structure :

```
├── ssdna-hic
    ├── data
        ├── inputs
        ├── outputs
        ├── references
        └── samples
```

- The ```samples``` dir contains all sparse matrix files.
- The ```references``` dir contains all reference files.
- The ```inputs``` dir contains all input files 
(samplesheet, capture oligos, fragments list, centromeres coordinates, etc.).

This pipeline aims to use to outputs of hicstuff to further analyze the data regarding the ssDNA HiC Capture protocol.

This pipeline allow to do the following analysis:

- Filter the contacts to keep only the reads containing the capture oligos.
- Compute the contacts coverage for each capture oligo.
- Output some statistics about the contacts with defined cis/trans region, intra/inter chromosomal regions.
- Normalize the contacts with those of a reference sample.
- Normalize contacts of ssdna probes with those of dsdna control probes.
- Create 4C like profiles for each probe (ssdna and dsdna). 
- Bin the probe contacts with the genome at different resolutions.
- Aggregate the contacts around the centromeres and telomeres.


You have to run the pipeline.py script with the following arguments:

```
python3 pipeline.py \
  < -s / --samplesheet > \
  < -o / --oligos-capture > \
  < -f / --fragments-list > \
  < -c / --centromeres-coordinates > \
  < -b / --binning-sizes > \
  < -a / --additional-groups > \
  < --window-size-centros > \
  < --window-size-telos >
  < --excluded-chr >
  < --exclude-probe-chr >
```

-  [ ] The ```samplesheet``` file is a ```.csv``` file that contains the samples to analyze.

| sample | reference1 | reference2 |
|--------|------------|------------|

**sample** : path to the sample sparse matrix file
**reference (optional)**: path to the reference file, in the case you want to weight the sample contacts. 
You can have as many reference col as you want. See reference file structure to see how to build reference file.


- [ ] The ```oligos-capture``` file is a ```.csv``` file that contains capture oligos related information
(similar but different from annealing oligos file used for ```oligos_replacement.py```).

| chr | start | end | type | name | sequence  |
|-----|-------|-----|------|------|-----------|

- [ ] The ```fragments-list``` file is a ```.txt``` file generated by hicstuff. See above for the structure.
- [ ] The ```centromeres-coordinates``` file is a ```.csv / .tsv``` file that contains the centromeres coordinates.
It must have the following structure:

| chr | length | left_arm_length | right_arm_length |
|-----|--------|-----------------|------------------|

left_arm_length and right_arm_length are the length of the left and right arm of the centromere. 
Can be *NaN* in the case of 2_micron or mitochondrial chromosome for instance.

- [ ] The ```binning-sizes``` a list of binning resolution you want for HiC contacts. Must be given as followed :

```-b 1000 2000 5000 10000 20000 50000 100000 ```

- [ ] The ```additional-groups``` file is a ```.csv``` file that contains the additional groups of probes
  (capture oligos) you wish to aggregate together for further analysis.


| name         | probes                    | action  |
|--------------|---------------------------|---------|
| average_left | probe1, probe2 ... probeN | average |
| sum_all      | probe1, probe2 ... probeN | sum     |

You can have as many additional groups as you want. The ```action``` column can be ```average``` or ```sum``` 
or whatever the aggregating operation you want to do on multiple probes at once.

- [ ] The ```window-size-centros``` is the size in bp of a focus centromeric region to aggregate data.
For instance :
```  --window-size-centros 150000```

the centromeric region is defined by *centromere bin - 150kb to centromere bin + 150kb*.

- [ ] The ```window-size-telos``` is the size in bp of a focus telomeric region to aggregate data.
For instance :
```  --window-size-telo 15000```
the telomeric regions (both extremities) are defined by *0 to 15kb* and  *chr's end - 150kb to chr's end*.

- [ ] The ```excluded-chr``` is a list of chromosomes you want to exclude from the analysis to avoid some bias.

``` --excluded-chr chr2 chr3 2_micron mitochondrion chr_artificial ```

- [ ] The ```exclude-probe-chr``` is a flag, if mentioned considered as True, else False. Allows to exclude the 
intra-chromosomal contacts (between the probes and its own chromosome) from the analysis to avoid some bias.

``` --exclude-probe-chr ``` to enable.


## TODO & Work in Progress :

- [ ] Package the project as a python package
- [ ] Make a docker image
- [ ] Make Web UI interface (run the app.py script to get an insight)
- [ ] Add a new script to generate the reference files based on WT samples
- [ ] Better overall handling of inputs files and parameters as well as outputs generated files.


