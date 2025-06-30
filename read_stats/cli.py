import argparse

# TODO: Introduce error handling # pylint: disable=fixme

def parse_args():
    parser = argparse.ArgumentParser(description="Compute read statistics from a BAM file.")
    parser.add_argument("--bam", help="Input BAM file")
    # parser.add_argument("bed", help="BED file with regions of interest")
    parser.add_argument("--output", help="Output folder for TSV and HTML file")
    return parser.parse_args()