import pysam as pys
import pandas as pd
import pyranges as pr
from read_stats.logging_config import setup_logger

logger = setup_logger(__name__)


def read_bam(bam_path):
    logger.debug("Attempting to read BAM file from: %s", bam_path)
    try:
        bam_file = pys.AlignmentFile(bam_path, "rb")
        # Perform a quick check to see if the file is valid
        if not bam_file.references:
            logger.warning("BAM file %s might be empty or headerless.", bam_path)
        logger.info("Successfully opened BAM file: %s", bam_path)
        return bam_file
    except FileNotFoundError:
        logger.error("BAM file not found: %s", bam_path)
        raise
    except ValueError as e:
        logger.error("Error reading BAM file %s: %s", bam_path, e, exc_info=True)
        raise

def check_overlap(stats, bed_file: str) -> pd.DataFrame:
    df = pd.DataFrame(stats)  
    if not bed_file:
        logger.info("No BED file specified. Skipping overlap computation.")
        df["Overlap"] = 0
        return df

    pr_df = df[["Chromosome", "Start", "End"]].copy()
    pr_df["index"] = df.index  # Keep track of original rows
    reads = pr.PyRanges(pr_df)
    bed = pr.read_bed(bed_file)
    overlapping = reads.overlap(bed)

    # Mark overlaps
    df["Overlap"] = 0
    if not overlapping.df.empty:
        df.loc[overlapping.df["index"], "Overlap"] = 1
    return df

# def load_bed(bed_path):
#     if not bed_path:
#         logger.info("No BED file specified. Skipping overlap computation.")
#         return None
    
#     logger.debug("Attempting to load BED file from: %s", bed_path)
    
#     try:
#         bed_tool = BedTool(bed_path)
#         if bed_tool.count() == 0:
#             logger.warning("BED file %s is empty or contains no valid regions.", bed_path)
#             return 0
#         logger.info("Successfully loaded BED file: %s", bed_path)
#         return bed_tool
#     except FileNotFoundError:
#         logger.error("BED file not found: %s", bed_path)
#         raise
#     except Exception as e: # pylint: disable=broad-exception-caught
#         logger.error("An unexpected error occurred while loading BED file %s: %s",
#                      bed_path, e, exc_info=True)
#         raise
    
# from pybedtools import BedTool
# def check_overlap(read_stat, bed_regions):
#     if not bed_regions:
#         read_stat["Overlap"] = 0
#         return read_stat
#     read_interval = BedTool([(read_stat['chrom'], read_stat['start'], read_stat['end'])])
#     print(read_interval)
#     overlaps_bed = read_interval.any_hits(bed_regions)
#     read_stat["Overlap"] = overlaps_bed
#     return read_stat
