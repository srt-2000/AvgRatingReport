"""Integration tests for report_factory.py"""

from __future__ import annotations

import os

import pytest

from src.report_factory import ReportFactory


class TestReportFactory:
    """Integration tests for ReportFactory.get_report()"""

    def test_get_report_brand_rating_single_file(self, temp_csv_files: dict[str, str]) -> None:
        """Test report generation with single file for brand/rating"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            # Generate report for brand/rating with single file
            result = ReportFactory.get_report(files=(temp_csv_files["file1"],), columns=("brand", "rating"))

            # Check that result is a string (table format)
            assert isinstance(result, str)

            # Check that table contains expected headers
            assert "brand" in result
            assert "rating" in result

            # Check that table contains data from first file
            assert "apple" in result
            assert "samsung" in result
            assert "xiaomi" in result

            # Check specific values from first file
            assert "4.9" in result  # iPhone 15 pro rating
            assert "4.8" in result  # Galaxy S23 ultra rating
            assert "4.6" in result  # Redmi note 12 rating

        finally:
            os.chdir(original_cwd)

    def test_get_report_brand_rating_multiple_files(
        self, temp_csv_files: dict[str, str], expected_brand_rating_report: list[dict[str, str | float]]
    ) -> None:
        """Test report generation with multiple files for brand/rating"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            # Generate report for brand/rating with multiple files
            result = ReportFactory.get_report(
                files=(temp_csv_files["file1"], temp_csv_files["file2"]), columns=("brand", "rating")
            )

            # Check that result is a string (table format)
            assert isinstance(result, str)

            # Check that table contains expected headers
            assert "brand" in result
            assert "rating" in result

            # Check that all brands are present
            assert "apple" in result
            assert "samsung" in result
            assert "xiaomi" in result

            # Check that expected average values are present
            for expected_item in expected_brand_rating_report:
                assert str(expected_item["brand"]) in result
                assert str(expected_item["rating"]) in result

        finally:
            os.chdir(original_cwd)

    def test_get_report_brand_price_multiple_files(self, temp_csv_files: dict[str, str]) -> None:
        """Test report generation with multiple files for brand/price"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            # Generate report for brand/price with multiple files
            result = ReportFactory.get_report(
                files=(temp_csv_files["file1"], temp_csv_files["file2"]), columns=("brand", "price")
            )

            # Check that result is a string (table format)
            assert isinstance(result, str)

            # Check that table contains expected headers
            assert "brand" in result
            assert "price" in result
            assert "rating" not in result  # Should not contain rating column

            # Check that all brands are present
            assert "apple" in result
            assert "samsung" in result
            assert "xiaomi" in result

            # Check that price values are present (averaged)
            # Apple: (999 + 429) / 2 = 714
            assert "714" in result
            # Samsung: (1199 + 999) / 2 = 1099
            assert "1099" in result
            # Xiaomi: (199 + 299) / 2 = 249
            assert "249" in result

        finally:
            os.chdir(original_cwd)

    def test_get_report_different_column_combinations(self, temp_csv_files: dict[str, str]) -> None:
        """Test report generation with different column combinations"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            # Test with name/rating combination
            result = ReportFactory.get_report(files=(temp_csv_files["file1"],), columns=("name", "rating"))

            assert isinstance(result, str)
            assert "name" in result
            assert "rating" in result
            assert "brand" not in result
            assert "price" not in result

        finally:
            os.chdir(original_cwd)


class TestReportFactoryEdgeCases:
    """Tests for edge cases and error handling"""

    def test_get_report_empty_files_tuple(self) -> None:
        """Test report generation with empty files tuple"""
        result = ReportFactory.get_report(files=(), columns=("brand", "rating"))

        # Should return empty table
        assert isinstance(result, str)
        assert result == ""

    def test_get_report_nonexistent_file(self, temp_csv_files: dict[str, str]) -> None:
        """Test report generation with non-existent file"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            # Should raise FileNotFoundError
            with pytest.raises(FileNotFoundError):
                ReportFactory.get_report(files=("nonexistent.csv",), columns=("brand", "rating"))

        finally:
            os.chdir(original_cwd)

    def test_get_report_mixed_existing_nonexistent_files(self, temp_csv_files: dict[str, str]) -> None:
        """Test report generation with mix of existing and non-existent files"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            # Should raise FileNotFoundError when it encounters non-existent file
            with pytest.raises(FileNotFoundError):
                ReportFactory.get_report(
                    files=(temp_csv_files["file1"], "nonexistent.csv"), columns=("brand", "rating")
                )

        finally:
            os.chdir(original_cwd)

    def test_get_report_single_record_data(self, temp_csv_files: dict[str, str]) -> None:
        """Test report generation with single record data"""
        # Create a file with single record
        single_record_data = """name,brand,price,rating
iphone,apple,999,4.5"""

        single_file_path = os.path.join(temp_csv_files["data_dir"], "single.csv")
        with open(single_file_path, "w") as f:
            f.write(single_record_data)

        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            result = ReportFactory.get_report(files=("single.csv",), columns=("brand", "rating"))

            assert isinstance(result, str)
            assert "brand" in result
            assert "rating" in result
            assert "apple" in result
            assert "4.5" in result

        finally:
            os.chdir(original_cwd)

    def test_get_report_all_same_brand(self, temp_csv_files: dict[str, str]) -> None:
        """Test report generation with all records having same brand"""
        # Create a file with all same brand
        same_brand_data = """name,brand,price,rating
iphone,apple,999,4.0
ipad,apple,799,4.5
macbook,apple,1999,5.0"""

        same_brand_file_path = os.path.join(temp_csv_files["data_dir"], "same_brand.csv")
        with open(same_brand_file_path, "w") as f:
            f.write(same_brand_data)

        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            result = ReportFactory.get_report(files=("same_brand.csv",), columns=("brand", "rating"))

            assert isinstance(result, str)
            assert "brand" in result
            assert "rating" in result
            assert "apple" in result
            # Average should be (4.0 + 4.5 + 5.0) / 3 = 4.5
            assert "4.5" in result

        finally:
            os.chdir(original_cwd)

    def test_get_report_table_format_verification(self, temp_csv_files: dict[str, str]) -> None:
        """Test that output is properly formatted table"""
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_csv_files["dir"])

            result = ReportFactory.get_report(files=(temp_csv_files["file1"],), columns=("brand", "rating"))

            # Check that it's a table format (contains grid characters)
            assert "+" in result or "|" in result or "-" in result

            # Check that it contains multiple lines (table structure)
            lines = result.split("\n")
            assert len(lines) > 1

            # Check that headers are present
            assert any("brand" in line.lower() for line in lines)
            assert any("rating" in line.lower() for line in lines)

        finally:
            os.chdir(original_cwd)
