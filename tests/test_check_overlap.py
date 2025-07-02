import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import pyranges as pr
from pandas.testing import assert_frame_equal
from read_stats.check_overlap import check_overlap

class TestCheckOverlap(unittest.TestCase):
    def setUp(self):
        # Example stats: chrom, start, end, name
        self.stats = [
            {"Chromosome": "chr1", "Start": 100, "End": 200, "Name": "read1"},
            {"Chromosome": "chr1", "Start": 300, "End": 400, "Name": "read2"},
            {"Chromosome": "chr2", "Start": 500, "End": 600, "Name": "read3"},
        ]
        self.df_stats = pd.DataFrame(self.stats)

    def test_no_bed_regions(self):
        # bed_regions is None
        result = check_overlap(self.stats, None)
        expected = self.df_stats.copy()
        expected["Overlap"] = 0
        assert_frame_equal(result, expected)

        # bed_regions is empty DataFrame
        empty_bed = pd.DataFrame(columns=["Chromosome", "Start", "End"])
        result = check_overlap(self.stats, empty_bed)
        assert_frame_equal(result, expected)
    
    def test_with_overlap(self):
        # Overlap with read2 only
        bed = pd.DataFrame({
            "Chromosome": ["chr1"],
            "Start": [350],
            "End": [360]
        })
        bed_regions = pr.PyRanges(bed)
        result = check_overlap(self.stats, bed_regions)
        expected = self.df_stats.copy()
        expected["Overlap"] = [0, 1, 0]
        assert_frame_equal(result, expected)

    def test_with_no_overlap(self):
        # No overlaps
        bed = pd.DataFrame({
            "Chromosome": ["chr1"],
            "Start": [1000],
            "End": [1100]
        })
        bed_regions = pr.PyRanges(bed)
        result = check_overlap(self.stats, bed_regions)
        expected = self.df_stats.copy()
        expected["Overlap"] = 0
        assert_frame_equal(result, expected)

if __name__ == "__main__":
    unittest.main()
