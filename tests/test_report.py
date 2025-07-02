import os
import tempfile
import unittest
import pandas as pd
from read_stats.report import write_simple_html, write_tsv

class TestReport(unittest.TestCase):
    def test_basic_html_output(self):
        df = pd.DataFrame([
            {
                "ReadID": "read1",
                "FragmentLength": 100,
                "AvgBaseQuality": 35.123,
                "GCContent": 48.5,
                "NumMismatches": 2,
                "Overlap": 1
            },
            {
                "ReadID": "read2",
                "FragmentLength": 90,
                "AvgBaseQuality": 30.0,
                "GCContent": 50.0,
                "NumMismatches": 0,
                "Overlap": 0
            }
        ])
        expected_html = (
            "<html><head><title>Read Stats</title></head><body>\n"
            "    <h1>Read Statistics</h1>\n"
            "    <p>Total Mapped Reads: 2</p>\n"
            "    <p>Overlapping Reads: 1</p>\n"
            "    <table border='1'>\n"
            "    <tr>\n"
            "        <th>ReadID</th>\n"
            "        <th>FragmentLength</th>\n"
            "        <th>AvgBaseQuality</th>\n"
            "        <th>GCContent</th>\n"
            "        <th>NumMismatches</th>\n"
            "    </tr>\n"
            "    <tr><td>read1</td><td>100</td><td>35.12</td><td>48.50</td><td>2</td></tr>\n"
            "<tr><td>read2</td><td>90</td><td>30.00</td><td>50.00</td><td>0</td></tr>\n"
            "</table></body></html>"
        )
        with tempfile.NamedTemporaryFile(delete_on_close=True, suffix=".html") as tmp:
            output_path = tmp.name
            write_simple_html(df, output_path)
            with open(output_path, "r", encoding="utf-8") as f:
                html = f.read()
                self.assertMultiLineEqual(html, expected_html)

    def test_empty_dataframe_html(self):
        df = pd.DataFrame(columns=["ReadID", "FragmentLength", "AvgBaseQuality", "GCContent", "NumMismatches", "Overlap"])
        expected_html = (
                "<html><head><title>Read Stats</title></head><body>\n"
                "    <h1>Read Statistics</h1>\n"
                "    <p>Total Mapped Reads: 0</p>\n"
                "    <p>Overlapping Reads: 0</p>\n"
                "    <table border='1'>\n"
                "    <tr>\n"
                "        <th>ReadID</th>\n"
                "        <th>FragmentLength</th>\n"
                "        <th>AvgBaseQuality</th>\n"
                "        <th>GCContent</th>\n"
                "        <th>NumMismatches</th>\n"
                "    </tr>\n"
                "    </table></body></html>"
            )
        with tempfile.NamedTemporaryFile(delete_on_close=True, suffix=".html") as tmp:
            output_path = tmp.name
            write_simple_html(df, output_path)
            with open(output_path, "r", encoding="utf-8") as f:
                html = f.read()
            self.assertMultiLineEqual(html, expected_html)

    def test_missing_values_html(self):
        df = pd.DataFrame([
            {
                "ReadID": "read3",
                "FragmentLength": 80,
                "AvgBaseQuality": None,
                "GCContent": None,
                "NumMismatches": None,
                "Overlap": 0
            }
        ])
        expected_html = (
                "<html><head><title>Read Stats</title></head><body>\n"
                "    <h1>Read Statistics</h1>\n"
                "    <p>Total Mapped Reads: 1</p>\n"
                "    <p>Overlapping Reads: 0</p>\n"
                "    <table border='1'>\n"
                "    <tr>\n"
                "        <th>ReadID</th>\n"
                "        <th>FragmentLength</th>\n"
                "        <th>AvgBaseQuality</th>\n"
                "        <th>GCContent</th>\n"
                "        <th>NumMismatches</th>\n"
                "    </tr>\n"
                "    <tr><td>read3</td><td>80</td><td></td><td></td><td></td></tr>\n"
                "</table></body></html>"
            )
        with tempfile.NamedTemporaryFile(delete_on_close=True, suffix=".html") as tmp:
            output_path = tmp.name
            write_simple_html(df, output_path)
            with open(output_path, "r", encoding="utf-8") as f:
                html = f.read()
                self.assertMultiLineEqual(html, expected_html)

    def test_basic_tsv_output(self):
        df = pd.DataFrame([
            {
                "ReadID": "read1",
                "FragmentLength": 100,
                "AvgBaseQuality": 35.123,
                "GCContent": 48.5,
                "NumMismatches": 2,
                "Overlap": 1
            },
            {
                "ReadID": "read2",
                "FragmentLength": 90,
                "AvgBaseQuality": 30.0,
                "GCContent": 50.0,
                "NumMismatches": 0,
                "Overlap": 0
            }
        ])
        expected_tsv = (
            "ReadID\tFragmentLength\tAvgBaseQuality\tGCContent\tNumMismatches\tOverlap\n"
            "read1\t100\t35.12\t48.50\t2\t1\n"
            "read2\t90\t30.00\t50.00\t0\t0\n"
        )
        with tempfile.NamedTemporaryFile(delete_on_close=True, suffix=".tsv") as tmp:
            output_path = tmp.name
            write_tsv(df, output_path)
            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertMultiLineEqual(content, expected_tsv)

    def test_empty_dataframe_tsv(self):
        df = pd.DataFrame(columns=["ReadID", "FragmentLength", "AvgBaseQuality", "GCContent", "NumMismatches", "Overlap"])
        with tempfile.NamedTemporaryFile(delete_on_close=True, suffix=".tsv") as tmp:
            output_path = tmp.name
            write_tsv(df, output_path)
            # Should not write anything, file should be empty or headerless
            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertEqual(content, "")

    def test_missing_values_tsv(self):
        df = pd.DataFrame([
            {
                "ReadID": "read3",
                "FragmentLength": 80,
                "AvgBaseQuality": None,
                "GCContent": None,
                "NumMismatches": None,
                "Overlap": 0
            }
        ])
        expected_tsv = (
            "ReadID\tFragmentLength\tAvgBaseQuality\tGCContent\tNumMismatches\tOverlap\n"
            "read3\t80\t\t\t\t0\n"
        )
        with tempfile.NamedTemporaryFile(delete_on_close=True, suffix=".tsv") as tmp:
            output_path = tmp.name
            write_tsv(df, output_path)
            with open(output_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertEqual(content, expected_tsv)