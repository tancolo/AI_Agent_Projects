# CSDN Blog Scraper

This project scrapes article metadata from a CSDN blog user (specifically `@shrimpcolo`) and saves it to a CSV file.

## Prerequisites

- Python 3.7+
- Chromium (installed via Playwright)

## Installation

1. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Playwright browser binaries:
   ```bash
   playwright install chromium
   ```

## Usage

Run the scraper:
```bash
python scraper.py
```

## Output

The script will generate `articles_data.csv` containing:
- Title
- Publish Date
- View Count
- Like Count
- Comment Count
- Bookmark Count
- Article URL
- Column/Series Name

## Note
The scraper handles infinite scrolling and visits each article page to extract the "Column" name, so it may take a few minutes to complete depending on the number of articles and network speed.
