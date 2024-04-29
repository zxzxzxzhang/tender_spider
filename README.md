
---

# Tender Information Web Scraper

This project is a web scraper tool for gathering tender information from the CCGP website, serving as a foundation for subsequent RAG analysis. It utilizes Requests for asynchronous web content retrieval and BeautifulSoup for webpage parsing.

## Key Features

- Supports specifying a range of page numbers for content retrieval.
- Saves results as an Excel file for easy analysis and processing.
- Saved file format is as follows:

| Title | Project Overview | One | Two | Three | Four | Five | Six | Seven | Eight | Nine | Attachment Link | Link |
|-------|----------------|-----|-----|------|------|------|-----|-------|-------|------|-----------------|------|
| xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx | xxxxx |

## Dependencies Installation

Before running the code, make sure you have installed the following dependencies:

- python==3.10
- beautifulsoup4==4.12.3
- pandas==2.2.1
- requests==2.31.0

You can install Python dependencies using the following commands:

```bash
pip install beautifulsoup4==4.12.3
pip install pandas==2.2.1
pip install requests==2.31.0
```

## Usage

1. Run the `Scraper.py` and `Scraper_all.py` files.
2. Variable settings:
   - `start_page`: Starting page for crawling
   - `end_page`: Ending page for crawling

---
