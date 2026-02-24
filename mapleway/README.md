# MapleWay 🍁

[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/tancolo/AI_Agent_Projects)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English] | [**简体中文**](./README_zh.md)

**MapleWay** is a professional browser extension designed for immigration applicants to the **Alberta Advantage Immigration Program (AAIP)**. It automates the extraction and analysis of complex processing data from the official Alberta government website, providing a clear and organized view of nomination quotas, draw history, and pool statistics.

### 🎥 Demo Video
![MapleWay Demo](https://github.com/tancolo/AI_Agent_Projects/raw/main/assets/demo_for_Mapleway.mp4)

> 💡 **Note**: If the video doesn't play above, you can [view/download it directly here](https://github.com/tancolo/AI_Agent_Projects/raw/main/assets/demo_for_Mapleway.mp4).

---

## 🌟 Key Features

### 🔍 Smart Data Scraping
- **Real-time Extraction**: Automatically scrapes the latest processing data from `alberta.ca`.
- **Historical Context**: Captures 2025 summaries and compares them with current 2026 data.
- **Deep Analysis**: Breaks down the "Process summary totals" (Allocation, Issued, Remaining, and Applications in progress).

### 🎯 Stream-Specific Insights
- **Targeted Filtering**: Select your specific stream (e.g., Alberta Opportunity Stream (AOS), Rural Renewal, Tourism and Hospitality) to see only the data relevant to you.
- **Detailed Metrics**: View specific nomination numbers and processing status for each pathway.

### 📊 Expression of Interest (EOI) & Draws
- **EOI Pool Tracking**: Monitor the "Expression of Interest" pool statistics (Table 8) with ease.
- **Draw History Analyzer**: Views the "Draw information" (Table 9) with integrated calculations.
- **Auto-Summarization**: Automatically calculates the total number of invitations across multiple draws for your selected stream.

---

## 🚀 Getting Started

### Prerequisites
- Google Chrome, Microsoft Edge, or any Chromium-based browser.

### Installation
1. **Download**: Clone or download this repository.
2. **Developer Mode**: Open your browser and go to `chrome://extensions/`. Enable **Developer mode** in the top right corner.
3. **Load**: Click **Load unpacked** and select the `/codebase/VanillaJS` directory within this project.
4. **Pin**: For easy access, pin the MapleWay extension to your browser toolbar.

### How to Use
1. Visit the [AAIP Processing Information Page](https://www.alberta.ca/aaip-processing-information).
2. Click the **MapleWay** icon.
3. Select your immigration stream from the dropdown.
4. Click **Analyze Page** to see the structured report.

---

## 📂 Project Structure

- `codebase/VanillaJS/`: Core extension source code (Manifest V3).
- `PRD/`: Detailed Product Requirement Documents and UI designs.
- `automated_test/`: Quality assurance scripts for data extraction accuracy.
- `icon_utils/`: Resources and scripts for extension iconography.
- `screenshots/`: Visual guides and feature demonstrations.

---

## 🛠 Tech Stack
- **Engine**: Vanilla JavaScript (ES6+)
- **UI**: CSS3 (Fluid layouts & Modern aesthetics)
- **Manifest**: Chrome Extension Manifest V3
- **Scraping**: DOM Parsing & Pattern Matching

---

## 📝 Roadmap
- [x] v0.1: Basic scraping for summaries and AOS.
- [x] v0.2: Enhanced EOI tracking and Draw calculation.
- [ ] v0.3: UI overhaul and multi-page support.
- [ ] Future: Data visualization charts and cloud sync.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contribution
Contributions are welcome! Please feel free to submit a Pull Request or open an Issue in the [Issues](./Issues) directory.

---

*Note: This extension is a third-party tool and is not affiliated with or endorsed by the Government of Alberta.*
