# Web Scraper V0.2

[中文版本 (Chinese Version)](README_CN.md)

## Overview
Web Scraper V0.2 is a multi-platform automated tool designed to aggregate article metadata from various technical blogs (CSDN, Jianshu, Juejin). It handles infinite scrolling, pagination, and detail extraction, then merges the data, de-duplicates it, translates titles from Chinese to English, and generates a structured Markdown report.

## Features
- **Multi-Platform Support**: Scrapes data from CSDN, Jianshu, and Juejin.
- **Unified Workflow**: A single entry point (`main_scraper.py`) to run the entire pipeline.
- **Robust Data Processing**: Deduplication across platforms and automated translation.
- **IPv4 Optimized Translation**: Fast translation using Google Translate bypasses IPv6 timeouts.
- **Progress Tracking**: Real-time progress countdown in the terminal (`Total - Processed = Remaining`).
- **Structured Output**: Clean CSV data and a professional Markdown report.

> [!NOTE]
> **Implementation Note**: In V0.2, the target blog user IDs (e.g., `shrimpcolo`) are currently hardcoded within each scraper script in `scraper_core/`. Support for external configuration files (e.g., `.ini` or `.yaml`) is planned for a future release to allow users to easily change the target accounts without modifying the code.

## Directory Structure
- `main_scraper.py`: The main entry point for the entire pipeline.
- `scraper_core/`: Contains the core logic for scraping each platform and post-processing.
  - `csdn_scraper.py`
  - `jianshu_scraper.py`
  - `juejin_scraper.py`
  - `merge_articles_data.py`: Merges CSVs and translates titles.
  - `generate_final_md.py`: Generates the final Markdown report.
- `scraper_output/`: Stores all generated products.
  - Platform-specific CSVs.
  - `merged_articles_final.csv`: The consolidated database.
  - `final_articles_report.md`: The final readable report.
- `scraper_debug/`: Contains test scripts and utilities used for debugging.

## Prerequisites
- Python 3.8+
- Chromium (installed via Playwright)

## Installation

1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Playwright browser binaries:
   ```bash
   playwright install chromium
   ```

## Configuration & Usage

The project is designed to be plug-and-play. You only need to run the main script from the root directory:

```bash
python main_scraper.py
```

### Script Execution Flow
1. **Scraping**: Calls the three platform scrapers sequentially. Browsers will open (headless=False) to ensure stability.
2. **Merging & Translating**: Combines the CSVs, removes duplicates based on titles, and uses an IPv4-forced patch to quickly translate titles.
3. **Report Generation**: Groups articles by column/category and writes to a Markdown file.

## Output
All results are saved in the `scraper_output/` folder. The primary output is `final_articles_report.md`, which contains links to all your articles organized by English category names.
