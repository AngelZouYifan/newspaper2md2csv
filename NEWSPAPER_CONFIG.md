# Newspaper Configuration Management

**IMPORTANT: The script processes ONE newspaper folder at a time.**

This system allows you to easily switch between different newspaper configurations by passing a parameter to the script.

## Quick Start

**Run the script with a specific newspaper:**
```bash
python pdfs2csv.py daily_nation_first100
python pdfs2csv.py business_daily
python pdfs2csv.py daily_nation_full
```

**List available newspapers:**
```bash
python pdfs2csv.py
```

The script will:
- Show which newspaper folder it's processing
- Only process PDF files in that specific folder
- Create CSV output for that newspaper only
- Display current configuration settings

## Available Newspapers

Currently configured newspapers:

1. **daily_nation_first100**
   - Folder: `data/Daily_Nation_first100/`
   - Agency: Daily Nation
   - Keywords: SGR, Standard Gauge Railway, railway, infrastructure, transport

2. **business_daily**
   - Folder: `data/Business Daily/`
   - Agency: Business Daily
   - Keywords: SGR, Standard Gauge Railway, national park, environment, pollution

3. **daily_nation_full**
   - Folder: `data/SGR Articles Daily Nation/`
   - Agency: Daily Nation
   - Keywords: SGR, Standard Gauge Railway, railway, infrastructure, transport, development

## Adding New Newspapers

To add a new newspaper configuration:

1. Edit `configs/newspaper_configs.json`
2. Add a new entry with the newspaper name as the key:

```json
{
  "my_newspaper": {
    "folder_name": "My Newspaper Folder",
    "agency": "My Newspaper Agency",
    "ignore_keywords": ["MY NEWSPAPER", "Some Keyword"],
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "header_delim": "〇〇〇",
    "header_placeholder": "〇〇〇",
    "date_regex": "(?:(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day[,\\s]*)?(January|February|March|April|May|June|July|August|September|October|November|December)[,\\s]*([1-9]|[12]\\d|3[01])[,\\s]*\\d{4}"
  }
}
```

### Configuration Fields

- **folder_name**: The folder name in your `data/` directory (must exist)
- **agency**: The newspaper agency name (appears in CSV output)
- **ignore_keywords**: Keywords to ignore when extracting headers (case-insensitive)
- **keywords**: Terms to search for in articles (case-insensitive, separated by semicolon in output)
- **header_delim**: Delimiter for headers in CSV output
- **header_placeholder**: Placeholder for headers in body text
- **date_regex**: Regular expression for extracting dates

## Date Regex Patterns

Different newspapers may use different date formats. Here are some common patterns:

- **Standard format**: `January 15, 2024`
- **With day**: `Monday, January 15, 2024`
- **Different separators**: `15/01/2024` or `15-01-2024`

The current regex pattern supports:
```
(?:(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day[,\s]*)?(January|February|March|April|May|June|July|August|September|October|November|December)[,\s]*([1-9]|[12]\d|3[01])[,\s]*\d{4}
```

This matches dates like:
- `January 15, 2024`
- `Monday, January 15, 2024`
- `January 15 2024`

## Processing Options

When you run the script, it will prompt for:

1. **Maximum lines per CSV file** (default: 1000)
   - Useful for managing large datasets
   - Creates multiple CSV files if needed

2. **Starting index** (default: 0)
   - Resume processing from a specific file
   - Useful if the script crashes or is interrupted

## Output Structure

The script creates CSV files with these columns:
- `file_name`: PDF filename without extension
- `newspaper_agency`: Agency name from configuration
- `date`: Extracted publication date
- `headers`: Article headers separated by the header delimiter
- `body`: Article body text with headers replaced by placeholders
- `keywords`: Found keywords separated by semicolons

## Error Handling

- **Missing folder**: Script will exit if the specified folder doesn't exist
- **No PDF files**: Script will exit if no PDF files are found
- **Configuration errors**: Script will show available newspapers and exit
- **Missing data**: Script will warn about files with missing dates, headers, or body text 