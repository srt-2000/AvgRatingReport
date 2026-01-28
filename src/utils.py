"""CSV data serialization utilities.

This module provides functionality for reading and parsing CSV files,
converting them into structured data format for further processing.
"""

from __future__ import annotations

import csv


class SerializeCSV:
    """Handles CSV file reading and data serialization.

    This class provides methods to read multiple CSV files and serialize
    their content into a unified list of dictionaries for further processing.

    Args:
        file_names: Tuple of CSV file names to process
    """

    def __init__(self, file_names: tuple[str, ...]) -> None:
        self.file_names: tuple[str, ...] = file_names
        self.full_data: list[dict] = []

    def get_full_data_from_files(self) -> list[dict]:
        """Read and serialize data from CSV files.

        Reads all specified CSV files and combines their data into a single
        list of dictionaries. Each dictionary represents one row from the CSV.

        Returns:
            List of dictionaries containing all data from CSV files

        Raises:
            FileNotFoundError: If any of the specified files doesn't exist
        """
        for file_name in self.file_names:
            with open(f"data/{file_name}") as csvfile:
                data = list(csv.DictReader(csvfile))
                self.full_data.extend(data)

        return self.full_data
