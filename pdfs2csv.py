import pymupdf4llm
import pathlib
import re
import csv
import os


##### Configuration #####
# TODO - modify based on newspaper
INPUT_PATH_STR = "Daily_Nation_first100" 
NEWSPAPER_AGENCY = "Daily Nation"
IGNORE_KEYWORDS = ["DAILY NATION", "National News"] # when extracting titles, ignore titles with these keywords

# MODIFY DELIMITERS
HEADER_DELIM = "〇〇〇"
HEADER_PLACEHOLDER = "〇〇〇"

# DO NOT CHANGE
INPUT_PATH = pathlib.Path(INPUT_PATH_STR)
OUTPUT_CSV = INPUT_PATH_STR+".csv"
FIELDNAMES = ["file_name", "newspaper_agency", "date", "headers", "body"]


HEADER_REGEX = re.compile(r"^(#{1,6})\s*(.+)$", re.MULTILINE)

DATE_REGEX = re.compile(
    r'(?:(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day[,\s]*)?'
    r'(January|February|March|April|May|June|July|August|September|October|November|December)'
    r'[,\s]*([1-9]|[12]\d|3[01])[,\s]*'
    r'\d{4}',
    re.IGNORECASE
)


def extract_date(text):
    # Strip bold, italics, inline code etc.
    clean_text = re.sub(r'(\*\*|\*|__|_|`)', '', text)
    match = DATE_REGEX.search(clean_text)
    return match.group(0) if match else None


##### Create CSV #####

# Write header only if file doesn't exist
if not os.path.exists(OUTPUT_CSV):
    with open(OUTPUT_CSV, "w", newline='', encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()


missing_count = 0

pdf_files = sorted(INPUT_PATH.glob("*.pdf"))

for i, pdf in enumerate(pdf_files):

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

    with open(OUTPUT_CSV, "a", newline='', encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)


    print(f"{i+1} files parsed")

    # record missing data
    if date == "" or headers == "" or body == "":
        print(f"Missing data in file: {pdf.name.rsplit('.', 1)[0]}")

        print(date)
        print(headers)
        print(body)
        missing_count += 1
        # if missing_count > 0:
        #     break
        continue
