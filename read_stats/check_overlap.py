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
    # Convert stats DataFrame to PyRanges
    reads = pr.PyRanges(df)
    overlapping = reads.overlap(bed_regions)

    # Mark overlaps
    if not overlapping.empty:
        df.loc[overlapping.index, "Overlap"] = 1
    return df