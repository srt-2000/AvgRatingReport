from __future__ import annotations

"""Report factory for generating various types of reports.

This module provides a factory class that integrates CSV data processing
and report generation components to create end-to-end report workflows.
"""

from src.reports import BrandReports
from src.utils import SerializeCSV


class ReportFactory:
    """Factory class for generating reports from CSV data.
    
    This class provides a unified interface for creating reports by
    integrating CSV data processing and report generation components.
    """
    
    @classmethod
    def get_report(cls, files: tuple[str, ...], columns: tuple[str, str]) -> str:
        """Generate a report from CSV files.
        
        Processes multiple CSV files and generates a report based on
        the specified column combination. This method orchestrates the
        entire workflow from data reading to report formatting.
        
        Args:
            files: Tuple of CSV file names to process
            columns: Tuple of column names for grouping and averaging
            
        Returns:
            Formatted report table as string
            
        Raises:
            FileNotFoundError: If any of the specified files doesn't exist
        """
        serializer = SerializeCSV(files)
        full_data = serializer.get_full_data_from_files()
        report = BrandReports(full_data, columns)
        return report.get_avg_rating_report()
