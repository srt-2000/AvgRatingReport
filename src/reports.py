"""Report generation functionality.

This module provides classes and methods for generating various types
of reports from product data, including average rating reports by brand.
"""

from __future__ import annotations

from collections import defaultdict

from tabulate import tabulate


class BrandReports:
    """Generates reports from product data.
    
    This class processes product data and generates various types of reports,
    such as average rating reports grouped by brand or other criteria.
    
    Args:
        full_data: List of dictionaries containing product data
        requested_columns: Tuple of column names for grouping and averaging
    """

    def __init__(self, full_data: list[dict], requested_columns: tuple[str, str]) -> None:
        self.full_data: list[dict] = full_data
        self.requested_columns: tuple[str, str] = requested_columns
        self.left_report_column: str = requested_columns[0]
        self.avg_column: str = requested_columns[1]
        self.values_data: defaultdict = defaultdict(list)
        self.grouped_request_data: list[dict] = []
        self.grouped_data: list[dict] = []

    def filter_by_report_columns(self) -> list[dict]:
        """Filter data to include only requested columns.
        
        Extracts only the specified columns from the full dataset,
        creating a filtered dataset for report generation.
        
        Returns:
            List of dictionaries containing only requested columns
        """
        for product in self.full_data:
            filtered_dict = {key: value for key, value in product.items() if key in self.requested_columns}
            self.grouped_request_data.append(filtered_dict)
        return self.grouped_request_data

    def group_by_avg(self) -> list[dict]:
        """Group data and calculate average values.
        
        Groups the filtered data by the left column and calculates
        average values for the right column. Results are sorted by
        average value in descending order.
        
        Returns:
            List of dictionaries with grouped data and average values
        """
        for product in self.grouped_request_data:
            left_column = product[self.left_report_column]
            report_column = product[self.avg_column]
            self.values_data[left_column].append(float(report_column))

        for left_column, report_column in self.values_data.items():
            avg_volume = round(sum(report_column) / len(report_column), 2)
            self.grouped_data.append({self.left_report_column: left_column, self.avg_column: avg_volume})

        self.grouped_data.sort(key=lambda x: x[self.avg_column], reverse=True)
        return self.grouped_data

    def get_avg_rating_report(self) -> str:
        """Generate formatted report table.
        
        Processes the data through filtering and grouping steps,
        then formats the result as a table using tabulate.
        
        Returns:
            Formatted table string ready for display
        """
        self.grouped_request_data = self.filter_by_report_columns()
        self.grouped_data = self.group_by_avg()
        return tabulate(self.grouped_data, headers="keys", tablefmt="grid")
