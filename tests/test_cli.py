import unittest
from unittest.mock import patch
import sys
import argparse
from read_stats.cli import parse_args

class TestCLI(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args_with_bam_and_output(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(bam="input.bam", output="output_folder", bed=None)
        # We need to set sys.argv because parse_args() will use it if parse_args is not mocked for other tests.
        # However, for *this* test, the mock_parse_args takes precedence.
        # Simulates command line arguments that would be passed to the script.
        with patch.object(sys, 'argv', ['read_stats/cli.py', '--bam', 'input.bam', '--output', 'output_folder']):
            args = parse_args()
            self.assertEqual(args.bam, "input.bam")
            self.assertEqual(args.output, "output_folder")
            self.assertIsNone(args.bed)
            # Check that parse_args was called (by the production code)
            mock_parse_args.assert_called_once()

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args_with_bam_output_and_bed(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(bam="input.bam", output="output_folder", bed="input.bed")
        with patch.object(sys, 'argv', ['read_stats/cli.py', '--bam', 'input.bam', '--output', 'output_folder', '--bed', 'input.bed']):
            args = parse_args()
            self.assertEqual(args.bam, "input.bam")
            self.assertEqual(args.output, "output_folder")
            self.assertEqual(args.bed, "input.bed")
            mock_parse_args.assert_called_once()

    @patch('sys.argv', ['read_stats/cli.py', '--bam', 'input.bam']) # Missing --output
    @patch('argparse.ArgumentParser.print_usage') # Suppress usage message during test
    def test_parse_args_missing_required_arguments(self, mock_print_usage):
        with patch('sys.stderr'):
            with self.assertRaises(SystemExit):
                parse_args()
        mock_print_usage.assert_called_once()

    @patch('sys.argv', ['read_stats/cli.py', '--output', 'out', '--bam', 'in.bam', '--unknown_arg', 'value'])
    @patch('argparse.ArgumentParser.print_usage') # Suppress usage message during test
    def test_parse_args_unknown_argument(self, mock_print_usage):
        with patch('sys.stderr'):
            with self.assertRaises(SystemExit):
                parse_args()
        mock_print_usage.assert_called_once()

if __name__ == '__main__':
    unittest.main()