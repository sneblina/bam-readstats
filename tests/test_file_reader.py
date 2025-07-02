# Test cases for io_utils.py
import unittest
from unittest.mock import patch, MagicMock
from read_stats.file_reader import read_bam, read_bed

# Placeholder for tests
class TestIOUtils(unittest.TestCase):
    @patch('read_stats.file_reader.pys.AlignmentFile')
    def test_read_bam_success(self, mock_alignment_file):
        mock_bam = MagicMock()
        mock_bam.references = ["chr1", "chr2"] # Simulate a valid BAM with references
        mock_alignment_file.return_value = mock_bam
        
        bam_file = read_bam("dummy.bam")
        
        mock_alignment_file.assert_called_once_with("dummy.bam", "rb")
        self.assertEqual(bam_file, mock_bam)

    @patch('read_stats.file_reader.pys.AlignmentFile')
    def test_read_bam_file_not_found(self, mock_alignment_file):
        mock_alignment_file.side_effect = FileNotFoundError("File not found")
        
        with self.assertRaises(FileNotFoundError):
            read_bam("nonexistent.bam")
        mock_alignment_file.assert_called_once_with("nonexistent.bam", "rb")

    @patch('read_stats.file_reader.pys.AlignmentFile')
    def test_read_bam_value_error(self, mock_alignment_file):
        mock_alignment_file.side_effect = ValueError("Invalid BAM format")
        
        with self.assertRaises(ValueError):
            read_bam("corrupted.bam")
        mock_alignment_file.assert_called_once_with("corrupted.bam", "rb")

    @patch('read_stats.file_reader.pr.read_bed')
    def test_read_bed_success(self, mock_read_bed):
        mock_bed = MagicMock()
        mock_read_bed.return_value = mock_bed
        
        bed_file = read_bed("dummy.bed")
        
        mock_read_bed.assert_called_once_with("dummy.bed")
        self.assertEqual(bed_file, mock_bed)
        
    @patch('read_stats.file_reader.pr.read_bed')
    def test_read_bed_file_not_found(self, mock_read_bed):
        mock_read_bed.side_effect = FileNotFoundError("File not found")
        
        with self.assertRaises(FileNotFoundError):
            read_bed("nonexistent.bed")
        mock_read_bed.assert_called_once_with("nonexistent.bed")
        
    @patch('read_stats.file_reader.pr.read_bed')
    def test_read_bed_value_error(self, mock_read_bed):
        mock_read_bed.side_effect = ValueError("Invalid BED format")
        
        with self.assertRaises(ValueError):
            read_bed("corrupted.bed")
        mock_read_bed.assert_called_once_with("corrupted.bed")

if __name__ == '__main__':
    unittest.main()
