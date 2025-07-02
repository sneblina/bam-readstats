import pysam as pys
import pyranges as pr
from read_stats.logging_config import setup_logger

logger = setup_logger(__name__)


def read_bam(bam_path):
    logger.debug("Attempting to read BAM file from: %s", bam_path)
    bam_file = pys.AlignmentFile(bam_path, "rb")
    logger.info("Successfully opened BAM file: %s", bam_path)
    return bam_file

def read_bed(bed_path):
    logger.debug("Attempting to read BED file from: %s", bed_path)
    bed_file = pr.read_bed(bed_path)
    logger.info("Successfully opened BED file: %s", bed_path)
    return bed_file