# bam-readstats

A Python tool for computing per-read statistics from BAM files, including fragment length, base quality, GC content, mismatches, and overlap with BED-defined regions. Outputs both tab-separated and HTML reports for downstream analysis or review in a browser.

## Features

- Computes per-read statistics from BAM files
- Supports optional overlap analysis with BED-defined regions
- Outputs results as both TSV and HTML reports
- Command-line interface for easy integration into pipelines

## Requirements

Python 3.12.4

## Installation

Clone the repository and install dependencies:

```
git clone https://github.com/yourusername/bam-readstats.git
cd bam-readstats

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

Run the tool with:

```
python -m read_stats --bam /path/to/file.bam --bed /path/to/file.bed --output /path/to/output/folder
```

- `--bam`: Path to the input BAM file (required)
- `--bed`: Path to the BED file for region overlap (optional)
- `--output`: Output directory must exists for reports (required)

## Output

- `output.html`: Interactive HTML report with per-read statistics
- `output.tsv`: Tab-separated file with all computed statistics

## Testing

Run unit tests with:

```
python -m unittest
```
