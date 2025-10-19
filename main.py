"""CLI entry point for AvgRatingReport application.

This module provides command-line interface for generating brand rating reports
from CSV files. It uses argparse for argument parsing and ReportFactory for
report generation.
"""

from __future__ import annotations

import argparse

from src.report_factory import ReportFactory

parser = argparse.ArgumentParser(description="Reports")
parser.add_argument("--files", nargs="+", type=str, dest="file_names", required=True, help="files list")
parser.add_argument("--report", type=str, dest="report_name", required=True, help="report name")
args = parser.parse_args()

if __name__ == "__main__":
    if not vars(args):
        parser.print_usage()
    if args.report_name == "average-rating":
        report_columns = ("brand", "rating")
        print(ReportFactory.get_report(tuple(args.file_names), report_columns))
    else:
        print("No such report")
