# bam-readstats
A Python tool for computing per-read statistics from BAM files, including fragment length, base quality, GC content, mismatches, and overlap with BED-defined regions. Outputs both tab-separated and HTML reports for downstream analysis or review in a browser.

## Usage

Run the tool with:

```
python -m bam-readstats --bam /path/to/file.bam --bed /path/to/file.bed --output /path/to/output/folder
```