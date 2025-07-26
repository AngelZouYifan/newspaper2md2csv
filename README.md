# Newspaper PDF to CSV Converter

A Python tool to convert newspaper PDF files to CSV format with extracted metadata including dates, headers, body text, and keyword detection.

## Installation

1. Install required dependencies:
```bash
pip install pymupdf4llm
```

2. Ensure your project structure is set up:
```
newspaper2md2csv/
├── data/                    # Place newspaper PDF folders here
├── configs/
│   └── newspaper_configs.json
├── sheets/                  # CSV output directory
└── pdfs2csv.py
```

## Quick Start

### 1. Add Newspaper PDFs and Update Configuration
Place your newspaper PDF files in folders within the `data/` directory. For example:
```
data/
├── Daily_Nation_first100/
├── Business Daily/
└── SGR Articles Daily Nation/
```

**Important**: After adding new newspaper folders, you must update the configuration file `configs/newspaper_configs.json` to include the new newspapers. See [[NEWSPAPER_CONFIG.md]] for detailed configuration instructions.

### 2. Run the Script
**Process a specific newspaper:**
```bash
python pdfs2csv.py daily_nation_first100
python pdfs2csv.py business_daily
python pdfs2csv.py daily_nation_full
```

**List available newspapers:**
```bash
python pdfs2csv.py invalid_name
```

### 3. Configuration
The script will prompt you for:
- Maximum lines per CSV file (default: 1000)
- Starting index for processing (useful for resuming after crashes)

## Output

The script generates CSV files with the following columns:
- `file_name`: Original PDF filename (without extension)
- `newspaper_agency`: Newspaper agency name
- `date`: Extracted publication date
- `headers`: Article headers (separated by 〇〇〇)
- `body`: Article body text
- `keywords`: Detected keywords from the content

## Features

- **Multi-newspaper support**: Process different newspapers with different configurations
- **Keyword detection**: Automatically finds specified keywords in articles
- **Date extraction**: Uses regex patterns to extract publication dates
- **Header filtering**: Ignores unwanted headers (e.g., newspaper mastheads)
- **Batch processing**: Handles large numbers of PDF files efficiently
- **Resume capability**: Start processing from any index if interrupted

## Configuration

Newspaper configurations are stored in `configs/newspaper_configs.json`. Each newspaper has:
- `folder_name`: Directory name in `data/`
- `agency`: Newspaper agency name
- `ignore_keywords`: Headers to exclude from extraction
- `keywords`: Terms to search for in articles
- `header_delim`: Delimiter for headers in CSV output
- `header_placeholder`: Placeholder text for headers in body
- `date_regex`: Regular expression for date extraction

## Troubleshooting

- **Missing data warnings**: Check if PDFs have proper text extraction
- **Resume processing**: Use the starting index parameter to continue from where you left off
- **Configuration errors**: Ensure `configs/newspaper_configs.json` is valid JSON

## Keywords

Common keywords for SGR (Standard Gauge Railway) articles:
- Standard Gauge Railway
- SGR
- Railway
- Infrastructure
- Transport
- Development
