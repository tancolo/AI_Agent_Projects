# MapleWay Browser Extension v0.1

🍁 **Alberta Advantage Immigration Program (AAIP) Data Scraper and Analyzer**

## Overview

MapleWay is a browser extension designed to help immigration applicants track and analyze data from the Alberta Advantage Immigration Program (AAIP). The extension scrapes relevant information from the official Alberta government website and presents it in an organized, easy-to-read format.

## Features

### v0.1 Features
- ✅ **2025 Summary**: Displays the total nominations issued in 2025
- ✅ **2026 Summary**: Shows current year allocation, issued nominations, remaining spots, and processing numbers
- ✅ **Stream-Specific Data**: Detailed information for selected immigration streams:
  - Alberta Opportunity Stream (AOS)
  - Rural Renewal Stream
  - Tourism and Hospitality Stream
  - Dedicated Health Care Pathways
  - Alberta Express Entry Stream
- ✅ **EOI Pool Data**: Expression of Interest pool statistics (Table 8)
- ✅ **Draw Information**: Historical draw data with automatic total calculations (Table 9)

## Installation

### Chrome/Edge Installation

1. **Download the Extension**
   - Navigate to `.\codebase\VanillaJS` folder

2. **Enable Developer Mode**
   - Open Chrome/Edge
   - Go to `chrome://extensions/` (or `edge://extensions/`)
   - Toggle "Developer mode" ON (top right corner)

3. **Load the Extension**
   - Click "Load unpacked"
   - Select the `.\codebase\VanillaJS` folder
   - The MapleWay extension should now appear in your extensions list

4. **Pin the Extension** (Optional)
   - Click the puzzle icon in the browser toolbar
   - Find "MapleWay" and click the pin icon

## Usage

1. **Navigate to the AAIP Page**
   - Go to: https://www.alberta.ca/aaip-processing-information

2. **Open the Extension**
   - Click the MapleWay icon in your browser toolbar

3. **Select Your Stream**
   - Choose your immigration stream from the dropdown menu
   - Example: "Alberta Opportunity Stream (AOS)"

4. **Analyze the Page**
   - Click the "Analyze Page" button
   - Wait for the extension to scrape and process the data

5. **Review Results**
   - View the organized data including:
     - Program summaries (2025 & 2026)
     - Stream-specific allocation details
     - EOI pool statistics
     - Draw information with calculated totals

## Technical Details

### Technology Stack
- **Language**: Vanilla JavaScript (ES6+)
- **Manifest**: Version 3
- **Permissions**: 
  - `activeTab`: Access to the current tab
  - `scripting`: Ability to inject content scripts
- **Host Permissions**: `https://www.alberta.ca/*`

### File Structure
```
VanillaJS/
├── manifest.json           # Extension configuration
├── icons/                  # Extension icons
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
├── popup/                  # Extension popup UI
│   ├── popup.html         # UI structure
│   ├── popup.css          # Styling
│   └── popup.js           # UI logic and data display
└── scripts/               # Content scripts
    └── content.js         # Web scraping logic
```

### How It Works

1. **Content Script** (`content.js`):
   - Injected into alberta.ca pages
   - Scrapes data from tables and text content
   - Responds to messages from the popup

2. **Popup Script** (`popup.js`):
   - Handles user interactions
   - Sends scraping requests to content script
   - Processes and displays received data
   - Calculates totals for draw information

3. **Message Passing**:
   - Chrome extension messaging API
   - Popup ↔ Content Script communication

## Data Extraction Details

### 2025 Summary
- Searches for paragraphs containing "AAIP issued" and "2025"
- Extracts the complete summary text

### 2026 Summary (Table 1)
- Locates "Process summary totals" table
- Extracts: Allocation, Issued, Remaining, Processing

### Stream-Specific Data
- Filters tables by selected stream name
- Extracts allocation details and notes

### EOI Pool (Table 8)
- Finds "Expression of interest pool" table
- Extracts all rows and columns

### Draw Information (Table 9)
- Locates "Draw information" table
- Filters by selected stream
- **Automatically calculates total invitations**
- Adds a "Total" row at the bottom

## Troubleshooting

### Extension Not Working
- Ensure you're on an alberta.ca page
- Check that the page contains the expected tables
- Try refreshing the page and reopening the extension

### No Data Displayed
- Verify you've selected a stream from the dropdown
- Check browser console for errors (F12 → Console)
- Ensure the page structure matches expected format

### Permission Errors
- Reload the extension from `chrome://extensions/`
- Ensure all permissions are granted

## Future Enhancements (Planned)

- 📊 Data visualization with charts
- 💾 Save and track historical data
- 🔔 Notifications for new draws
- 📤 Export data to CSV/Excel
- 🌐 Support for multiple languages

## Development

### Prerequisites
- Modern web browser (Chrome, Edge, Brave, etc.)
- Basic understanding of JavaScript and browser extensions

### Testing
1. Make changes to the code
2. Go to `chrome://extensions/`
3. Click the refresh icon on the MapleWay extension
4. Test the changes on the target website

## License

This project is for educational and personal use.

## Support

For issues or questions, please refer to the PRD documentation in the `PRD` folder.

---

**Version**: 0.1.0  
**Last Updated**: January 2026  
**Developed with**: Vanilla JavaScript + Manifest V3
