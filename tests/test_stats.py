import unittest
from unittest.mock import Mock, patch
from Bio.SeqUtils import gc_fraction
from read_stats.stats import compute_avg_quality, compute_stats

class TestStats(unittest.TestCase):
    def test_compute_avg_quality_with_base_qualities(self):
        base_qualities = [10, 20, 30, 40]
        self.assertEqual(compute_avg_quality(base_qualities), 25.0)

    def test_compute_avg_quality_empty_list(self):
        qualities = []
        self.assertEqual(compute_avg_quality(qualities), 0)

    def test_compute_stats_typical_read(self):
        mock_read = Mock()
        mock_read.is_unmapped = False
        mock_read.query_name = "read1"
        mock_read.template_length = 200
        mock_read.query_qualities = [10, 20, 30, 40]
        mock_read.query_sequence = "AGCT"
        mock_read.has_tag.return_value = True
        mock_read.get_tag.return_value = 1
        mock_read.reference_name = "chr1"
        mock_read.reference_start = 100
        mock_read.reference_end = 300

        expected_stats = {
            "ReadID": "read1",
            "FragmentLength": 200,
            "AvgBaseQuality": 25.0,
            "GCContent": 0.5,
            "NumMismatches": 1,
            "Chromosome": "chr1",
            "Start": 100,
            "End": 300
        }
        self.assertEqual(compute_stats(mock_read), expected_stats)
        mock_read.has_tag.assert_called_once_with("NM")
        mock_read.get_tag.assert_called_once_with("NM")

    def test_compute_stats_unmapped_read(self):
        mock_read = Mock()
        mock_read.is_unmapped = True
        mock_read.query_name = "read2"
        self.assertIsNone(compute_stats(mock_read))

    def test_compute_stats_no_qualities(self):
        mock_read = Mock()
        mock_read.is_unmapped = False
        mock_read.query_name = "read3"
        mock_read.template_length = 150
        mock_read.query_qualities = [] # No qualities
        mock_read.query_sequence = "GATTACA"
        mock_read.has_tag.return_value = True
        mock_read.get_tag.return_value = 0
        mock_read.reference_name = "chrX"
        mock_read.reference_start = 1000
        mock_read.reference_end = 1150

        stats = compute_stats(mock_read)
        self.assertEqual(stats["AvgBaseQuality"], 0)


    def test_compute_stats_missing_nm_tag(self):
        mock_read = Mock()
        mock_read.is_unmapped = False
        mock_read.query_name = "read5"
        mock_read.template_length = 120
        mock_read.query_qualities = [25, 28, 30]
        mock_read.query_sequence = "ATGC"
        mock_read.has_tag.return_value = False # NM tag missing
        mock_read.reference_name = "chrY"
        mock_read.reference_start = 200
        mock_read.reference_end = 320

        stats = compute_stats(mock_read)
        self.assertIsNone(stats["NumMismatches"])
        mock_read.has_tag.assert_called_once_with("NM")
        mock_read.get_tag.assert_not_called()

    @patch('read_stats.stats.gc_fraction')
    def test_compute_stats_exception_handling(self, mock_gc_fraction):
        mock_read = Mock()
        mock_read.is_unmapped = False
        mock_read.query_name = "read5"
        mock_read.template_length = 120
        mock_read.query_qualities = [25, 28, 30]
        mock_read.query_sequence = "ATGC"
        mock_read.has_tag.return_value = False # NM tag missing
        mock_read.reference_name = "chrY"
        mock_read.reference_start = 200
        mock_read.reference_end = 320
        mock_gc_fraction.side_effect = ValueError("Test error on gc_fraction")

        with self.assertLogs('read_stats.stats', level='ERROR') as cm:
            with self.assertRaises(ValueError) as context_manager:
                compute_stats(mock_read)
        
        self.assertTrue(any("Error processing read read5" in log for log in cm.output))
        self.assertEqual(str(context_manager.exception), "Test error on gc_fraction")


if __name__ == '__main__':
    unittest.main()
