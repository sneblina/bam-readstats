import pandas as pd
import pyranges as pr
from read_stats.logging_config import setup_logger

logger = setup_logger(__name__)

def check_overlap(stats, bed_regions):
    df = pd.DataFrame(stats)
    df["Overlap"] = 0
    if bed_regions is None or bed_regions.empty:
        logger.info("No BED file specified. Skipping overlap computation.")
        return df

    pr_df = df[["Chromosome", "Start", "End"]].copy()
    pr_df["index"] = df.index  # Keep track of original rows
    reads = pr.PyRanges(pr_df)
    overlapping = reads.overlap(bed_regions)

    # Mark overlaps
    if not overlapping.empty:
        df.loc[overlapping["index"], "Overlap"] = 1
    return df