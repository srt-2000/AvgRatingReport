"""Unit tests for reports.py"""

from __future__ import annotations

from src.reports import BrandReports


class TestBrandReportsInit:
    """Tests for BrandReports initialization"""

    def test_init_with_valid_data(self, sample_product_data: list[dict[str, str]]) -> None:
        """Test initialization with valid data"""
        requested_columns = ("brand", "rating")
        report = BrandReports(sample_product_data, requested_columns)

        # Check attributes
        assert report.full_data == sample_product_data
        assert report.requested_columns == requested_columns
        assert report.left_report_column == "brand"
        assert report.avg_column == "rating"
        assert report.values_data == {}
        assert report.grouped_request_data == []
        assert report.grouped_data == []

    def test_init_with_different_columns(self, sample_product_data: list[dict[str, str]]) -> None:
        """Test initialization with different column combination"""
        requested_columns = ("brand", "price")
        report = BrandReports(sample_product_data, requested_columns)

        assert report.left_report_column == "brand"
        assert report.avg_column == "price"


class TestFilterByReportColumns:
    """Tests for filter_by_report_columns method"""

    def test_filter_brand_rating_columns(self, sample_product_data: list[dict[str, str]]) -> None:
        """Test filtering by brand and rating columns"""
        report = BrandReports(sample_product_data, ("brand", "rating"))
        result = report.filter_by_report_columns()

        # Check that only requested columns are present
        for item in result:
            assert set(item.keys()) == {"brand", "rating"}

        # Check that all original records are preserved
        assert len(result) == len(sample_product_data)

        # Check specific values
        assert result[0] == {"brand": "apple", "rating": "4.9"}
        assert result[1] == {"brand": "samsung", "rating": "4.8"}

    def test_filter_brand_price_columns(self, sample_product_data: list[dict[str, str]]) -> None:
        """Test filtering by brand and price columns"""
        report = BrandReports(sample_product_data, ("brand", "price"))
        result = report.filter_by_report_columns()

        # Check that only requested columns are present
        for item in result:
            assert set(item.keys()) == {"brand", "price"}

        # Check specific values
        assert result[0] == {"brand": "apple", "price": "999"}
        assert result[1] == {"brand": "samsung", "price": "1199"}

    def test_filter_empty_data(self):
        """Test filtering with empty data"""
        report = BrandReports([], ("brand", "rating"))
        result = report.filter_by_report_columns()

        assert result == []
        assert len(result) == 0


class TestGroupByAvg:
    """Tests for group_by_avg method"""

    def test_group_by_brand_rating(self, sample_product_data: list[dict[str, str]]) -> None:
        """Test grouping by brand and calculating average rating"""
        report = BrandReports(sample_product_data, ("brand", "rating"))
        report.filter_by_report_columns()
        result = report.group_by_avg()

        # Check that we have 3 unique brands
        assert len(result) == 3

        # Check specific calculations
        brand_ratings = {item["brand"]: item["rating"] for item in result}

        # Apple: (4.9 + 4.1) / 2 = 4.5
        assert brand_ratings["apple"] == 4.5

        # Samsung: (4.8 + 4.6) / 2 = 4.7
        assert brand_ratings["samsung"] == 4.7

        # Xiaomi: (4.6 + 4.4) / 2 = 4.5
        assert brand_ratings["xiaomi"] == 4.5

    def test_group_by_brand_price(self, sample_product_data: list[dict[str, str]]) -> None:
        """Test grouping by brand and calculating average price"""
        report = BrandReports(sample_product_data, ("brand", "price"))
        report.filter_by_report_columns()
        result = report.group_by_avg()

        # Check that we have 3 unique brands
        assert len(result) == 3

        # Check specific calculations
        brand_prices = {item["brand"]: item["price"] for item in result}

        # Apple: (999 + 429) / 2 = 714.0
        assert brand_prices["apple"] == 714.0

        # Samsung: (1199 + 999) / 2 = 1099.0
        assert brand_prices["samsung"] == 1099.0

        # Xiaomi: (199 + 299) / 2 = 249.0
        assert brand_prices["xiaomi"] == 249.0

    def test_group_with_single_record(self):
        """Test grouping with single record"""
        data = [{"brand": "apple", "rating": "4.5"}]
        report = BrandReports(data, ("brand", "rating"))
        report.filter_by_report_columns()
        result = report.group_by_avg()

        assert len(result) == 1
        assert result[0] == {"brand": "apple", "rating": 4.5}

    def test_group_with_same_brand_multiple_ratings(self):
        """Test grouping with same brand having multiple ratings"""
        data = [
            {"brand": "apple", "rating": "4.0"},
            {"brand": "apple", "rating": "4.5"},
            {"brand": "apple", "rating": "5.0"},
        ]
        report = BrandReports(data, ("brand", "rating"))
        report.filter_by_report_columns()
        result = report.group_by_avg()

        assert len(result) == 1
        # (4.0 + 4.5 + 5.0) / 3 = 4.5
        assert result[0] == {"brand": "apple", "rating": 4.5}


class TestGetAvgRatingReport:
    """Tests for get_avg_rating_report method"""

    def test_full_report_generation(
        self, sample_product_data: list[dict[str, str]], expected_brand_rating_report: list[dict[str, str | float]]
    ) -> None:
        """Test complete report generation"""
        report = BrandReports(sample_product_data, ("brand", "rating"))
        result = report.get_avg_rating_report()

        # Check that result is a string (table format)
        assert isinstance(result, str)

        # Check that table contains headers
        assert "brand" in result
        assert "rating" in result

        # Check that table contains expected data
        for expected_item in expected_brand_rating_report:
            assert str(expected_item["brand"]) in result
            assert str(expected_item["rating"]) in result

    def test_report_with_different_columns(self, sample_product_data: list[dict[str, str]]) -> None:
        """Test report generation with different column combination"""
        report = BrandReports(sample_product_data, ("brand", "price"))
        result = report.get_avg_rating_report()

        # Check that result is a string
        assert isinstance(result, str)

        # Check that table contains correct headers
        assert "brand" in result
        assert "price" in result
        assert "rating" not in result

    def test_report_with_empty_data(self) -> None:
        """Test report generation with empty data"""
        report = BrandReports([], ("brand", "rating"))
        result = report.get_avg_rating_report()

        # Should return empty table with headers
        assert isinstance(result, str)
        # With empty data, tabulate returns empty string, so we check for empty result
        assert result == ""


class TestBrandReportsEdgeCases:
    """Tests for edge cases and error handling"""

    def test_single_record_data(self) -> None:
        """Test with single record"""
        data = [{"name": "iphone", "brand": "apple", "price": "999", "rating": "4.5"}]
        report = BrandReports(data, ("brand", "rating"))
        result = report.get_avg_rating_report()

        assert isinstance(result, str)
        assert "apple" in result
        assert "4.5" in result

    def test_all_same_brand(self) -> None:
        """Test with all records having same brand"""
        data = [
            {"brand": "apple", "rating": "4.0"},
            {"brand": "apple", "rating": "4.5"},
            {"brand": "apple", "rating": "5.0"},
        ]
        report = BrandReports(data, ("brand", "rating"))
        result = report.get_avg_rating_report()

        assert isinstance(result, str)
        assert "apple" in result
        # Average should be (4.0 + 4.5 + 5.0) / 3 = 4.5
        assert "4.5" in result

    def test_decimal_precision(self) -> None:
        """Test decimal precision in calculations"""
        data = [{"brand": "apple", "rating": "4.33"}, {"brand": "apple", "rating": "4.67"}]
        report = BrandReports(data, ("brand", "rating"))
        report.filter_by_report_columns()
        result = report.group_by_avg()

        # (4.33 + 4.67) / 2 = 4.5, should be rounded to 2 decimal places
        assert result[0]["rating"] == 4.5

    def test_float_conversion(self) -> None:
        """Test that string values are properly converted to float"""
        data = [{"brand": "apple", "rating": "4.5"}, {"brand": "apple", "rating": "3.5"}]
        report = BrandReports(data, ("brand", "rating"))
        report.filter_by_report_columns()
        result = report.group_by_avg()

        # Should handle string to float conversion correctly
        assert result[0]["rating"] == 4.0  # (4.5 + 3.5) / 2 = 4.0
