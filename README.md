
---

# Tender Information Web Scraper

This project is a web scraper tool for gathering tender information, serving as a foundation for subsequent RAG analysis. It utilizes Requests for asynchronous web content retrieval and BeautifulSoup for webpage parsing.

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

1. Run the `run.py` file, and set the following variables:
   - `start_page`: Starting page number for scraping.
   - `end_page`: Ending page number for scraping.
   - `wait1`: Minimum value for the random interval.
   - `wait2`: Maximum value for the random interval.

## Example

Here is an example (`run.py`) that scrapes pages from 1 to 2 and saves the results as an Excel file:

```python
from Scraper_all import main

start_page = 1
end_page = 2
wait1 = 1
wait2 = 1

main(start_page=start_page, end_page=end_page, wait1=wait1, wait2=wait2)
```
---
