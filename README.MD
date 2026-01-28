# AvgRatingReport

A Python script for analyzing brand ratings from CSV files. The tool processes product data and generates average rating reports by brand.

## Features

- **Multi-file processing**: Analyze data from multiple CSV files simultaneously
- **Flexible reporting**: Generate reports based on different column combinations
- **Table output**: Clean, formatted table display using tabulate
- **Extensible architecture**: Easy to add new report types

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd AvgRatingReport

# Install dependencies using Poetry
poetry install
```

## Usage

### Basic Usage

```bash
python main.py --files products1.csv products2.csv --report average-rating
```

### Parameters

- `--files`: List of CSV files to process (required)
- `--report`: Report type to generate (required)

### Data store

Files must be stored in a project folder
```/data/```
If its necessary to use another data store, you have to change directory path in utils.SerializeCSV().get_full_data_from_files()
```
    def get_full_data_from_files(self) -> list[dict]:
        ...
            with open(f"data/{file_name}") as csvfile:
        ...
```

### Example Output

```
+---------+----------+
| brand   |   rating |
+=========+==========+
| apple   |     4.55 |
+---------+----------+
| samsung |     4.53 |
+---------+----------+
| xiaomi  |     4.37 |
+---------+----------+
```

## CSV File Format

The script expects CSV files with the following columns:
- `name`: Product name
- `brand`: Brand name
- `price`: Product price
- `rating`: Product rating

Example:
```csv
name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
```

## Adding New Report Types

To add a new report type (e.g., average price by brand):

1. **Add new condition in `main.py`:**
```python
elif args.report_name == "average-price":
    report_columns = ("brand", "price")
    print(ReportFactory.get_report(tuple(args.file_names), report_columns))
```

2. **The architecture automatically handles:**
   - Data filtering by specified columns
   - Grouping and averaging calculations
   - Table formatting

## Testing

Run the test suite:

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=term-missing

# Run specific test file
poetry run pytest tests/test_utils.py -v
```

## Project Structure

```
AvgRatingReport/
├── src/
│   ├── utils.py          # CSV data serialization
│   ├── reports.py        # Report generation logic
│   └── report_factory.py # Integration layer
├── tests/
│   ├── conftest.py       # Test fixtures
│   ├── test_utils.py     # Unit tests for utils
│   ├── test_reports.py   # Unit tests for reports
│   └── test_report_factory.py # Integration tests
├── data/
│   ├── products1.csv     # Sample data
│   └── products2.csv     # Sample data
├── main.py               # CLI entry point
└── pyproject.toml        # Project configuration
```

## Architecture

The project follows a clean, modular architecture:

- **`SerializeCSV`**: Handles CSV file reading and data serialization
- **`BrandReports`**: Processes data and generates reports
- **`ReportFactory`**: Integrates components for end-to-end report generation
- **`main.py`**: CLI interface using argparse

## Requirements

- Python 3.12+
- Poetry (for dependency management)
- Standard libraries only (argparse, csv)
- tabulate (for table formatting)
- pytest (for testing)
- ruff (for code linting and formatting)

## Tech Stack

### Core
- **Python 3.12+** - Programming language
- **Poetry** - Dependency management and packaging

### Libraries
- **tabulate** - Table formatting and display
- **pytest** - Testing framework
- **pytest-cov** - Code coverage reporting
- **ruff** - Fast Python linter and code formatter

### Standard Libraries
- **argparse** - Command-line interface parsing
- **csv** - CSV file reading and parsing
- **collections** - Data structures for grouping and aggregation

### Build Tools
- **poetry-core** - Build backend for Poetry projects

## Development

### Code Quality
- 100% test coverage
- Type hints throughout
- PEP 8 compliance (enforced by ruff)
- Code formatting with ruff
- Comprehensive error handling

## 👨‍💻 Author

- **Name:** srt-2000
- **Email:** srt2000888@gmail.ru
