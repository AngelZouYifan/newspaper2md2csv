
1. Install pymupdf4llm `pip install pymupdf4llm`

2. Add newspaper into data folder

3. In `pdfs2csv.py`. Change the following parameters accordingly

```
# TODO - modify based on newspaper
INPUT_PATH_STR = "Daily_Nation_first100" 
NEWSPAPER_AGENCY = "Daily Nation"
IGNORE_KEYWORDS = ["DAILY NATION", "National News"] # when extracting titles, ignore titles with these keywords
```


Note:
L91 `print(f"{i+1} files parsed")` - Start over after this index if program crashes

Keywords:
Standard Gauge Railway 
SGR
