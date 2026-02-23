# Web Scraper V0.3

[中文版本 (Chinese Version)](README_CN.md)

## Overview
Web Scraper V0.3 is a multi-platform automated tool designed to aggregate article metadata from various technical blogs (CSDN, Jianshu, Juejin). It handles infinite scrolling, pagination, and detail extraction, then merges the data, de-duplicates it, translates titles from Chinese to English, and generates a structured Markdown report.

## Features
- **Multi-Platform Support**: Scrapes data from CSDN, Jianshu, and Juejin.
- **Unified Workflow**: A single entry point (`main_scraper.py`) to run the entire pipeline.
- **Robust Data Processing**: Deduplication across platforms and automated translation.
- **IPv4 Optimized Translation**: Fast translation using Google Translate bypasses IPv6 timeouts.
- **Progress Tracking**: Real-time progress countdown in the terminal (`Total - Processed = Remaining`).
- **Structured Output**: Clean CSV data and a professional Markdown report.
- **Configuration-Driven**: Target URLs and output directories are fully manageable via an external `config.json` file.
- **Standalone Mode**: Scraper scripts can be run and tested independently from the command line while still reading the main configuration.

> [!NOTE]
> **V0.3 Updates**: Hardcoded platform URLs have been successfully removed from `scraper_core/` files. You can now easily duplicate configurations or change source URLs in the project's root `config.json` file.

## Directory Structure
- `config.json`: The central configuration file mapping platforms to URLs and export paths.
- `main_scraper.py`: The orchestrator that reads `config.json` and sequentially runs enabled platform scrapers.
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

The project is highly configurable. Open `config.json` in the root directory to set `"enabled": true/false`, configure source `url`s, and rename outputs.

### Pipeline Execution
To run all enabled scrapers followed by the deduplication and report generation steps:
```bash
python main_scraper.py
```

### Standalone Scraper Execution
To test or scrape data for a single platform:
```bash
python scraper_core/csdn_scraper.py
python scraper_core/jianshu_scraper.py
python scraper_core/juejin_scraper.py
```
Each script will automatically parse `config.json` for its properties.

### Script Execution Flow
1. **Scraping**: Loads configurations and conditionally invokes the three platform scrapers. Browsers will open (headless=False).
2. **Merging & Translating**: Combines the CSVs, removes duplicates based on titles, and uses an IPv4-forced patch to quickly translate titles.
3. **Report Generation**: Groups articles by column/category and writes to a Markdown file.

## Output
All results are saved in the `scraper_output/` folder. The primary output is `final_articles_report.md`, which contains links to all your articles organized by English category names.
