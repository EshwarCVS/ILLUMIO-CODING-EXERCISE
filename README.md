# Flow Log Parser

This project parses AWS VPC flow logs and maps each row to a tag based on a lookup table.

## Requirements

- Python 3.7+
- No external dependencies required

## Installation

1. Clone the repository:

git clone https://github.com/EshwarCVS/illumio.coding-exercise.git
cd illumio-coding-exercise

2. (Optional) Create a virtual environment:

python -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate

## Usage

Run the script with the following command:
python src/flow_log_parser.py <flow_log_file> <lookup_file> <output_file>

For example:
python src/flow_log_parser.py tests/sample_flow_log.txt tests/sample_lookup.csv output.csv

## Running Tests

To run the unit tests:
python -m unittest discover tests

## Output

The script generates a CSV file containing:
- Count of matches for each tag
- Count of matches for each port/protocol combination

## Assumptions

- The flow log file is in the default format (only parses version 2) as specified in the AWS documentation.
- The lookup table CSV file has three columns: dstport, protocol, and tag.
- The matches are case-insensitive for the protocol. Here we are considering to make everything to lowercase.
- IANA Protocol Number Mapping: Correctly handle protocol numbers as per the IANA list from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
- If a flow doesn't match any tag in the lookup table, it's counted as "untagged".

## Standards and Best Practices

This project follows these standards and best practices:
- PEP 8 for Python code style
- Type hinting for improved code readability and maintainability
- Modularity: Split logic into separate functions to keep the code clean and maintainable.
- Logging for better debugging and error tracking
- Argparse for command-line argument parsing
- CSV module for reading and writing CSV files
- Efficiency: Use dictionaries for O(1) lookups, making the solution scalable for large datasets
- Unit testing with Python's unittest framework
- Documentation: Include comprehensive details in the README.md for easy setup and execution.
- Clear project structure separating source code and tests