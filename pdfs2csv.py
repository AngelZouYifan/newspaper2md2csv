import pymupdf4llm
import pathlib
import re
import csv
import os
import math
import json
import sys


##### Helper Functions #####
def extract_date(text):
    # Strip bold, italics, inline code etc.
    clean_text = re.sub(r'(\*\*|\*|__|_|`)', '', text)
    match = DATE_REGEX.search(clean_text)
    return match.group(0) if match else None


def get_csv_filename(base_name, file_number):
    """Generate CSV filename with number suffix if needed"""
    if file_number == 1:
        return f"{base_name}.csv"
    else:
        return f"{base_name}_part{file_number}.csv"


def write_csv_header(filename):
    """Write CSV header to the specified file"""
    with open(filename, "w", newline='', encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()


def write_csv_row(filename, row):
    """Write a single row to the specified CSV file"""
    with open(filename, "a", newline='', encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)


def get_user_input(prompt, min_value=1, max_value=None, default=None):
    """Get validated user input with optional default value"""
    while True:
        try:
            if default is not None:
                user_input = input(f"{prompt} (default: {default}): ").strip()
                if user_input == "":
                    return default
            else:
                user_input = input(f"{prompt}: ").strip()
            
            value = int(user_input)
            
            if value < min_value:
                print(f"Value must be at least {min_value}")
                continue
                
            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}")
                continue
                
            return value
            
        except ValueError:
            print("Please enter a valid number")


##### Configuration #####
def load_newspaper_config(newspaper_name=None):
    """Load newspaper configuration from JSON file."""
    try:
        with open("configs/newspaper_configs.json", "r", encoding="utf-8") as f:
            configs = json.load(f)

        print("Available newspapers:")
        for name in configs.keys():
            print(f"  {name}")
        
        # Use provided newspaper name or default
        if newspaper_name is None or newspaper_name not in configs.keys():
            return None
        
        return configs[newspaper_name]
        
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"Error loading config: {e}")
        return None

# Parse command line arguments
def parse_arguments():
    """Parse command line arguments for newspaper selection."""
    if len(sys.argv) > 1:
        newspaper_name = sys.argv[1]
        print(f"Using newspaper: {newspaper_name}")
        return newspaper_name
    else:
        print("No newspaper specified. Using default configuration.")
        return None

# Get newspaper name from command line
newspaper_name = parse_arguments()

# Load configuration
config = load_newspaper_config(newspaper_name)
if config is None:
    print("Error: Could not load newspaper configuration.")
    print("Please check your configs/newspaper_configs.json file.")
    exit(1)

NEWSPAPER_FOLDER_NAME = config["folder_name"]
NEWSPAPER_AGENCY = config["agency"]
IGNORE_KEYWORDS = config["ignore_keywords"]
HEADER_DELIM = config["header_delim"]
HEADER_PLACEHOLDER = config["header_placeholder"]

# DO NOT CHANGE
INPUT_PATH = pathlib.Path("data/" + NEWSPAPER_FOLDER_NAME)
OUTPUT_CSV_BASE = NEWSPAPER_FOLDER_NAME
FIELDNAMES = ["file_name", "newspaper_agency", "date", "headers", "body"]

HEADER_REGEX = re.compile(r"^(#{1,6})\s*(.+)$", re.MULTILINE)
DATE_REGEX = re.compile(config["date_regex"], re.IGNORECASE)

# Display current newspaper configuration
print("="*60)
print(f"PROCESSING NEWSPAPER: {NEWSPAPER_AGENCY}")
print(f"FOLDER: {NEWSPAPER_FOLDER_NAME}")
print(f"IGNORE KEYWORDS: {IGNORE_KEYWORDS}")
print("="*60)


##### Main Processing #####

# Check if input folder exists
if not INPUT_PATH.exists():
    print(f"ERROR: Input folder '{INPUT_PATH}' does not exist!")
    print(f"Please ensure the folder 'data/{NEWSPAPER_FOLDER_NAME}' exists and contains PDF files.")
    print("\nTo switch to a different newspaper, use:")
    print(f"  python switch_newspaper.py list")
    print(f"  python switch_newspaper.py switch <newspaper_name>")
    exit(1)

# Get all PDF files and print total count
pdf_files = sorted(INPUT_PATH.glob("*.pdf"))
total_files = len(pdf_files)
print(f"Total number of PDF files found: {total_files}")

if total_files == 0:
    print(f"No PDF files found in '{INPUT_PATH}'.")
    print("Please ensure the folder contains PDF files.")
    exit(1)

# Get user input for max lines per CSV
print(f"\nFound {total_files} PDF files to process.")
max_lines = get_user_input(
    f"Enter maximum number of lines per CSV file", 
    min_value=100, 
    max_value=total_files,
    default=1000
)
MAX_LINES_PER_CSV = max_lines

# Get user input for starting index
print(f"\nFiles will be processed from index 0 to {total_files-1}")
start_index = get_user_input(
    f"Enter the starting index (0-{total_files-1})", 
    min_value=0, 
    max_value=total_files-1,
    default=0
)

# Calculate how many CSV files we'll need for the remaining files
remaining_files = total_files - start_index
total_csv_files = math.ceil(remaining_files / MAX_LINES_PER_CSV)
print(f"\nWill process {remaining_files} files starting from index {start_index}")
print(f"Will create {total_csv_files} CSV file(s) with max {MAX_LINES_PER_CSV} lines each")

# Initialize CSV file tracking
current_csv_file = 1
current_line_count = 0
current_csv_filename = get_csv_filename(OUTPUT_CSV_BASE, current_csv_file)

# Write header to first CSV file
write_csv_header(current_csv_filename)

missing_count = 0

# Process files starting from the specified index
for i in range(start_index, total_files):
    pdf = pdf_files[i]
    print(f"Processing file {i+1}/{total_files}: {pdf.name}")

    md_text = pymupdf4llm.to_markdown(str(pdf))

    # Extract date
    date = extract_date(md_text)

    # Extract headers, filter unwanted ones
    headers_raw = HEADER_REGEX.findall(md_text)
    headers = [title.strip() for _, title in headers_raw
               if not any(kw.lower() in title.lower() for kw in IGNORE_KEYWORDS)]

    # Replace headers in body with placeholder
    def header_sub(m):
        title = m.group(2).strip()
        if any(kw.lower() in title.lower() for kw in IGNORE_KEYWORDS):
            return ""
        return HEADER_PLACEHOLDER

    body = HEADER_REGEX.sub(header_sub, md_text).strip()

    row = {
        "file_name": pdf.name.rsplit('.', 1)[0],
        "newspaper_agency": NEWSPAPER_AGENCY,
        "date": date,
        "headers": HEADER_DELIM.join(headers),
        "body": body
    }

    # Check if we need to start a new CSV file
    if current_line_count >= MAX_LINES_PER_CSV:
        current_csv_file += 1
        current_line_count = 0
        current_csv_filename = get_csv_filename(OUTPUT_CSV_BASE, current_csv_file)
        write_csv_header(current_csv_filename)
        print(f"Created new CSV file: {current_csv_filename}")

    # Write the row to current CSV file
    write_csv_row(current_csv_filename, row)
    current_line_count += 1

    # Record missing data
    if not date or not headers or not body:
        print(f"Missing data in file: {pdf.name.rsplit('.', 1)[0]}")
        print(f"  Date: {date}")
        print(f"  Headers: {headers}")
        print(f"  Body length: {len(body)}")
        missing_count += 1

print(f"\nProcessing complete!")
print(f"Files processed: {remaining_files} (from index {start_index} to {total_files-1})")
print(f"Files with missing data: {missing_count}")
print(f"CSV files created: {current_csv_file}")
