# Python Automation Mini-Projects

Two ready-to-run scripts:

## 1) PDF Merger
- Merge many PDFs into one.
- Handles encrypted PDFs (with `--password`), sorts by name/mtime/size.

**Run**
```bash
pip install -r requirements.txt
python pdf_merger.py -i a.pdf b.pdf -o merged.pdf
python pdf_merger.py -d ./pdfs -o merged.pdf --sort name
```

## 2) Generic Web Scraper
- CSS selector based, no hardcoding.
- Export to CSV/JSON/NDJSON.
- Works for links, images, product cards etc.

**Run**
```bash
pip install -r requirements.txt

# Example: collect all links from a page
python web_scraper.py --url https://example.com --select a --attr href --out links.csv

# Example: scrape Books to Scrape
python web_scraper.py --url https://books.toscrape.com \
  --item ".product_pod" \
  --field "title:h3 a@title" \
  --field "price:.price_color@text" \
  --field "link:h3 a@href" \
  --resolve-urls \
  --out books.csv
```
