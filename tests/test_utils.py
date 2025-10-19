"""Unit tests for utils.py"""

from __future__ import annotations

import os

import pytest

from src.utils import SerializeCSV


class TestSerializeCSVMultipleFiles:
    """Tests for reading multiple files and data merging"""

    def test_read_multiple_files_success(
        self, temp_csv_files: dict[str, str], sample_product_data: list[dict[str, str]]
    ) -> None:
        """Test successful reading of multiple files"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            # Create instance with two files
            serializer = SerializeCSV((temp_csv_files["file1"], temp_csv_files["file2"]))

            # Read data
            result = serializer.get_full_data_from_files()

            # Check record count
            assert len(result) == 6, f"Expected 6 records, got {len(result)}"

            # Check data structure
            expected_keys = {"name", "brand", "price", "rating"}
            for row in result:
                assert set(row.keys()) == expected_keys, f"Invalid keys in row: {row}"

            # Check data order (first file, then second)
            assert result[0]["name"] == "iphone 15 pro"  # First record from first file
            assert result[3]["name"] == "poco x5 pro"  # First record from second file

            # Check specific values
            assert result[0] == sample_product_data[0]
            assert result[3] == sample_product_data[3]

        finally:
            os.chdir(original_cwd)

    def test_read_multiple_files_with_empty_file(
        self, temp_csv_files: dict[str, str], empty_csv_file: dict[str, str]
    ) -> None:
        """Test reading files including empty file"""
        # Copy empty file to first fixture's data folder
        import shutil

        shutil.copy2(empty_csv_file["file_path"], os.path.join(temp_csv_files["data_dir"], empty_csv_file["file"]))

        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            # Create instance with file and empty file
            serializer = SerializeCSV((temp_csv_files["file1"], empty_csv_file["file"]))

            # Read data
            result = serializer.get_full_data_from_files()

            # Check record count (only from first file, empty file adds no records)
            assert len(result) == 3, f"Expected 3 records, got {len(result)}"

            # Check that data is only from first file
            assert result[0]["name"] == "iphone 15 pro"
            assert result[1]["name"] == "galaxy s23 ultra"
            assert result[2]["name"] == "redmi note 12"

        finally:
            os.chdir(original_cwd)

    def test_read_same_file_multiple_times(self, temp_csv_files: dict[str, str]) -> None:
        """Test reading same file multiple times"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            # Create instance with same file twice
            serializer = SerializeCSV((temp_csv_files["file1"], temp_csv_files["file1"]))

            # Read data
            result = serializer.get_full_data_from_files()

            # Check that data is duplicated
            assert len(result) == 6, f"Expected 6 records (3*2), got {len(result)}"

            # Check duplication
            assert result[0] == result[3]  # First record repeats
            assert result[1] == result[4]  # Second record repeats
            assert result[2] == result[5]  # Third record repeats

        finally:
            os.chdir(original_cwd)

    def test_full_data_accumulation(self, temp_csv_files: dict[str, str]) -> None:
        """Test data accumulation in full_data on repeated calls"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            serializer = SerializeCSV((temp_csv_files["file1"], temp_csv_files["file2"]))

            # First call
            result1 = serializer.get_full_data_from_files()
            assert len(result1) == 6

            # Second call - data should accumulate
            result2 = serializer.get_full_data_from_files()
            assert len(result2) == 12, f"Expected 12 records (6*2), got {len(result2)}"

            # Check that data accumulates (first 6 records from first call)
            expected_first_6 = [
                {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
                {"name": "galaxy s23 ultra", "brand": "samsung", "price": "1199", "rating": "4.8"},
                {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
                {"name": "poco x5 pro", "brand": "xiaomi", "price": "299", "rating": "4.4"},
                {"name": "iphone se", "brand": "apple", "price": "429", "rating": "4.1"},
                {"name": "galaxy z flip 5", "brand": "samsung", "price": "999", "rating": "4.6"},
            ]

            # Check that first 6 records match expected
            assert result2[:6] == expected_first_6

            # Check that last 6 records duplicate first 6
            assert result2[6:] == expected_first_6

        finally:
            os.chdir(original_cwd)

    def test_file_not_found_error(self, temp_csv_files: dict[str, str]) -> None:
        """Test error handling for non-existent file"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            # Create instance with non-existent file
            serializer = SerializeCSV(("nonexistent.csv", temp_csv_files["file1"]))

            # Should raise error
            with pytest.raises(FileNotFoundError):
                serializer.get_full_data_from_files()

        finally:
            os.chdir(original_cwd)

    def test_empty_file_names_tuple(self) -> None:
        """Test with empty file names tuple"""
        serializer = SerializeCSV(())

        # Should return empty list
        result = serializer.get_full_data_from_files()
        assert result == []
        assert len(result) == 0

    def test_data_structure_consistency(self, temp_csv_files: dict[str, str]) -> None:
        """Test data structure consistency from different files"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            serializer = SerializeCSV((temp_csv_files["file1"], temp_csv_files["file2"]))
            result = serializer.get_full_data_from_files()

            # Check that all records have same structure
            expected_keys = {"name", "brand", "price", "rating"}
            for i, row in enumerate(result):
                assert set(row.keys()) == expected_keys, f"Invalid keys in record {i}: {row}"

                # Check that all values are strings (as from CSV)
                for key, value in row.items():
                    assert isinstance(value, str), f"Value {key} is not a string: {type(value)}"

        finally:
            os.chdir(original_cwd)
