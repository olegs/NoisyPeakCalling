# NoisyPeakCalling

## Project description

ChIP-sequencing is a method used to analyze protein interactions with DNA. The reads obtained from sequencing are mostly aligned on a regions where a protein interacts with DNA. The goal of __peak calling__ algorithm is to identify such enriched areas (__peaks__) in a genome.

According to Jung2014[[1]](#jung), derived set of peaks could vary depending on sequencing depth and specific algorithm. In the paper only sequencing depth was considered; here we analyze an impact of noise in ChIP-seq data on peak calling algorithms performance.   

## Goals and objectives

The aims of the project:
1. To study ChIP-seq protocol and Jung2014 paper.
2. To acquire noisy data for an experiment.
3. To analyse the influence of noise on __MACS2__[[2]](#macs2), __SICER__[[3]](#sicer) and __SPAN__[[4]](#span) peak calling algorithms.

## Methods
### Data

For experiment we choose five H3 histone modifications: [__H3K4me1__](https://www.encodeproject.org/files/ENCFF076WOE/), [__H3K4me3__](https://www.encodeproject.org/files/ENCFF001FYS/), [__H3K27ac__](https://www.encodeproject.org/files/ENCFF000CEN/), [__H3K27me3__](https://www.encodeproject.org/files/ENCFF001FYR/), [__H3K36me3__](https://www.encodeproject.org/files/ENCFF000CFB/), control files [ENCFF825XKT](https://www.encodeproject.org/files/ENCFF825XKT/) (for H3K4me1), [ENCFF001HUV](https://www.encodeproject.org/files/ENCFF001HUV/) (for H3K4me3 and H3K27me3), [ENCFF692GVG](https://www.encodeproject.org/files/ENCFF692GVG/) (for H3K27ac and H3K36me3) and [reference](https://www.encodeproject.org/files/GRCh38_no_alt_analysis_set_GCA_000001405.15/) for alignment. All the files were obtained from the ENCODE project[[5]](#encode) site. Biosample is human CD14-positive monocyte cells. 

We use:
- bowtie2 (version 2.3.4.3) for reads alignment;
- samtools (1.9) for sorting and filtering;
- bamCoverage from deeptools package (version 3.2.1) to obtain bigWig files;
- bamtobed from bedtools package (version 2.28.0) to obtain bed files from alignment;
- sambamba (version 0.6.6) for mixing ChIP-seq and control reads.

All the commands for alignment have standard settings.

### Project scripts

`prepare_dataset.sh` takes as input _[data_folder]_ _[ref]_, where
- _data_folder_ is an existing directory with .fastq files you want to align
- _ref_ is a .fasta file with reference for your data. 

The script aligns and indexes all the .fastq files in _data_folder_ using _ref_ as reference.

`peakcalling.sh`  takes as input _[chip]_ _[control]_ _[n_reads]_ _[name]_ _[peakcaller]_ _[fdr]_, where
- _chip_ is aligned chip-seq reads
- _control_ is aligned control reads
- _n_reads_ is number of reads to choose for experiment (should be less then number of reads both in chip and control)
- _name_ is a name for output file (recommended to be a modification name)
- _peakcaller_ is a peakcalling algorithm (now available macs2, sicer and span)

It mixes the reads from _chip_ and _control_ in proportion from 0% to 90% of control and runs _peakcaller_ on mixed file. Now it is possible to choose only _fdr_ parameter for running. 

`signal_to_noise_estimation.py` takes as input _[file]_ _[-d fragment_size]_  _[OPTIONS]_, where
- _[file]_ is a path to file in .bam format
- _-d_ is a size of chip fragment (you could obtain it from macs2 logs, for example)

The script counts signal-to-noise ratio as ratio of 90 to 10 percentiles of genome bin coverage distribution (90 to 10 is default settings, but I recommend you to set first number to larger value, like 95% or 99%).

`result_visualization.py` is a set of functions that draw plots with different statistics of result data. Running `$ python3  result_visualization.py` would draw the main results graphs. All the pictures available in /result/ folder

`project_structure.py` and `jbr_gb_data.py` are necessary for result visualisation and contains structure of folders with peak calling data and tracks overlapping data from JBR Genome browser respectively.

`peaks_dynamics.py` contains the set of functions for calculating different statistics, necessary for result visualization.

`join_files.sh` is a supplementary script, that is runned by `peakcalling.sh` to mix chip and control with specified proportion.

### Project pipeline

- Download files listed in __data__ 
- Run `conda env create -f env.yaml` to get all the required programs
- Run `./prepare_data.sh` to align your ChIP-seq and control reads
- Run `./peakcalling.sh` to obtain noisy peak calling data
- Get peak overlapping info from JBR Genome Browser and write it in `jbr_gb_data.py`. More detailed instructions could be found in that file.
- Run `result_visualization.py` to get graphs for your data. Note that you don't need to follow the whole pipeline to obtain results:  
    - for _figures 1-2_ from __results__ one could use `plot_peaks_dynamics()` wich requires only files from `./peakcalling.sh`
    - for _figures 3-5_ functions `plot_true_peaks_comparison()` and `plot_peak_set_comparison()` require only genome browser data (they are already listed for given dataset)

## Results

The following plots shows that increasing level of noise leads to decreasing in number of peaks and its average length.
![](https://github.com/DaryaChaplygina/NoisyPeakCalling/blob/master/result/n_peaks_fdr_FDR%200.05.png?raw=true)
![](https://github.com/DaryaChaplygina/NoisyPeakCalling/blob/master/result/len_peaks_fdr_FDR%200.05.png?raw=true)
_<p align="center">Figure 1-2</p>_


Visualization of true peaks (i.e. peaks, which algorithm could find in file with 0% of noise) percentage in peakcaller output shows that __SPAN is the most stable to noisy data__ and __lower FDR level leads to lower stability__.

![](https://github.com/DaryaChaplygina/NoisyPeakCalling/blob/master/result/pk_colors.png?raw=true)
![](https://github.com/DaryaChaplygina/NoisyPeakCalling/blob/master/result/true_peaks_dynamics.png?raw=true)
_<p align="center">Figure 3</p>_

Next barplots present percentage of overlapping peaks in reakcallers results. Bars are splitted into three groups for MACS2, SICER and SPAN respectively, and the higher bar is, the more peaks from other algorithm are embedded into peaks of the current. These plots shows that __SPAN data with FDR0.05 is the most consistent__ and __higher noise level leads to lower peaks sets similarity__.  

![](https://github.com/DaryaChaplygina/NoisyPeakCalling/blob/master/result/noise_colors.png?raw=true)
#### FDR 0.05
![](https://github.com/DaryaChaplygina/NoisyPeakCalling/blob/master/result/plot_peak_set_comparison_fdr_FDR%200.05.png?raw=true)
_<p align="center">Figure 4</p>_

#### FDR 1e-6
![](https://github.com/DaryaChaplygina/NoisyPeakCalling/blob/master/result/plot_peak_set_comparison_fdr_FDR%201E-6.png?raw=true)
_<p align="center">Figure 5</p>_

## References 

<a name="jung">[1]</a>  Jung YL, Luquette LJ, Ho JW, et al. Impact of sequencing depth in ChIP-seq experiments. Nucleic Acids Res. 2014;42(9):e74. doi:10.1093/nar/gku178

<a name="macs2">[2]</a>  Zhang Y, Liu T, Meyer CA, et al. Model-based analysis of ChIP-Seq (MACS). Genome Biol. 2008;9(9):R137. doi:10.1186/gb-2008-9-9-r137

<a name="sicer">[3]</a>  Xu S, Grullon S, Ge K, Peng W. Spatial clustering for identification of ChIP-enriched regions (SICER) to map regions of histone methylation patterns in embryonic stem cells. Methods Mol Biol. 2014;1150:97–111. doi:10.1007/978-1-4939-0512-6_5

<a name="span">[4]</a> SPAN Semi-supervised Peak Analyzer https://github.com/JetBrains-Research/span

<a name="encode">[5]</a>  Encyclopedia of DNA Elements. https://www.encodeproject.org/
