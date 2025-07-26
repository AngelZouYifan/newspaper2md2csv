import pymupdf4llm
import pathlib
import re


INPUT_PATH = pathlib.Path("Daily_Nation_first100")
OUTPUT_PATH = pathlib.Path("Daily_Nation_first100_md")
OUTPUT_PATH.mkdir(exist_ok=True)

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

def create_md():
    # create markdown files
    for pdf_name in pdf_list:
        pdf = pathlib.Path(pdf_name)

        in_path = INPUT_PATH / pdf
        md_text = pymupdf4llm.to_markdown(str(in_path))

        date = extract_date(md_text)
        print(pdf.name)
        print(date)

        out_path = OUTPUT_PATH / pdf.name.replace(".pdf", ".md")
        out_path.write_bytes(md_text.encode())


def check_md():
    # check date in markdown files
    for pdf_name in pdf_list:
        pdf = pathlib.Path(pdf_name)

        md_file = OUTPUT_PATH / pdf.name.replace(".pdf", ".md")
        md_text = md_file.read_text(encoding="utf-8")

        date = extract_date(md_text)
        print(pdf.name)
        print(date)

# pdf_files = sorted(INPUT_PATH.glob("*.pdf"))[:20]
# for pdf in pdf_files:
#     md_text = pymupdf4llm.to_markdown(str(pdf))
#     out_path = OUTPUT_PATH / pdf.name.replace(".pdf", ".md")
#     out_path.write_bytes(md_text.encode())


pdf_list = ["003DNC1812.pdf"]

create_md()
check_md()