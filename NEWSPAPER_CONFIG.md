# Newspaper Configuration Management

**IMPORTANT: The script processes ONE newspaper folder at a time.**

This system allows you to easily switch between different newspaper configurations by passing a parameter to the script.

## Quick Start

**Run the script with a specific newspaper:**
```bash
python pdfs2csv.py daily_nation_first100
python pdfs2csv.py business_daily
python pdfs2csv.py sgr_articles
```

**Run with default newspaper (if no parameter provided):**
```bash
python pdfs2csv.py
```

The script will:
- Show which newspaper folder it's processing
- Only process PDF files in that specific folder
- Create CSV output for that newspaper only

## Available Newspapers

To see available newspapers, run the script with an invalid name:
```bash
python pdfs2csv.py invalid_name
```

This will show you the list of available newspaper configurations.

## Adding New Newspapers

To add a new newspaper configuration:

1. Edit `configs/newspaper_configs.json`
2. Add a new entry under `"newspapers"` with:
   - `folder_name`: The folder name in your `data/` directory
   - `agency`: The newspaper agency name
   - `ignore_keywords`: Keywords to ignore when extracting headers
   - `header_delim`: Delimiter for headers in CSV output
   - `header_placeholder`: Placeholder for headers in body text
   - `date_regex`: Regular expression for extracting dates

Example:
```json
{
  "newspapers": {
    "my_newspaper": {
      "folder_name": "My Newspaper Folder",
      "agency": "My Newspaper Agency",
      "ignore_keywords": ["MY NEWSPAPER", "Some Keyword"],
      "header_delim": "〇〇〇",
      "header_placeholder": "〇〇〇",
      "date_regex": "(?:(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day[,\\s]*)?(January|February|March|April|May|June|July|August|September|October|November|December)[,\\s]*([1-9]|[12]\\d|3[01])[,\\s]*\\d{4}"
    }
  },
  "current_newspaper": "my_newspaper"
}
```

## Date Regex Patterns

Different newspapers may use different date formats. Here are some common patterns:

- **Standard format**: `January 15, 2024`
- **With day**: `Monday, January 15, 2024`
- **Different separators**: `15/01/2024` or `15-01-2024`

Adjust the `date_regex` field in your configuration to match your newspaper's date format. 