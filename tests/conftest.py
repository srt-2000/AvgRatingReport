"""Fixtures for testing utils.py"""

from __future__ import annotations

import os
import shutil
import tempfile

import pytest


@pytest.fixture
def temp_csv_files():
    """Creates temporary CSV files for testing"""
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()

    # Create data folder
    data_dir = os.path.join(temp_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    # Data for first file
    csv1_data = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6"""

    # Data for second file
    csv2_data = """name,brand,price,rating
poco x5 pro,xiaomi,299,4.4
iphone se,apple,429,4.1
galaxy z flip 5,samsung,999,4.6"""

    # Create files directly in data folder
    file1_path = os.path.join(data_dir, "test_products1.csv")
    file2_path = os.path.join(data_dir, "test_products2.csv")

    with open(file1_path, "w") as f:
        f.write(csv1_data)
    with open(file2_path, "w") as f:
        f.write(csv2_data)

    yield {
        "dir": temp_dir,
        "data_dir": data_dir,
        "file1": "test_products1.csv",
        "file2": "test_products2.csv",
        "file1_path": file1_path,
        "file2_path": file2_path,
    }

    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_product_data():
    """Sample product data for testing - contains 6 products with name, brand, price, rating"""
    return [
        {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
        {"name": "galaxy s23 ultra", "brand": "samsung", "price": "1199", "rating": "4.8"},
        {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
        {"name": "poco x5 pro", "brand": "xiaomi", "price": "299", "rating": "4.4"},
        {"name": "iphone se", "brand": "apple", "price": "429", "rating": "4.1"},
        {"name": "galaxy z flip 5", "brand": "samsung", "price": "999", "rating": "4.6"},
    ]


@pytest.fixture
def empty_csv_file():
    """Creates empty CSV file with headers"""
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()

    # Create data folder
    data_dir = os.path.join(temp_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    # Create empty file in data folder
    file_path = os.path.join(data_dir, "empty.csv")
    with open(file_path, "w") as f:
        f.write("name,brand,price,rating\n")

    yield {"dir": temp_dir, "data_dir": data_dir, "file": "empty.csv", "file_path": file_path}

    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def expected_brand_rating_report():
    """Expected results for brand rating report"""
    return [
        {"brand": "apple", "rating": 4.5},  # (4.9 + 4.1) / 2 = 4.5
        {"brand": "samsung", "rating": 4.7},  # (4.8 + 4.6) / 2 = 4.7
        {"brand": "xiaomi", "rating": 4.5},  # (4.6 + 4.4) / 2 = 4.5
    ]
