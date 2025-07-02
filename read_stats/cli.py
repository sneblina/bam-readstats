import argparse
from read_stats.logging_config import setup_logger

logger = setup_logger(__name__)
# logging.basicConfig(level=logging.INFO)

def parse_args():
    logger.debug("Parsing command line arguments.")
    parser = argparse.ArgumentParser(description="Compute read statistics from a BAM file.")
    parser.add_argument("--bam", help="Input BAM file", required=True)
    parser.add_argument("--bed", help="BED file with regions of interest")
    parser.add_argument("--output", help="Output folder for TSV and HTML file", required=True)
    args = parser.parse_args()
    logger.debug("Arguments parsed: %s", args)
    return args