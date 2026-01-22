// Content script to scrape AAIP data from alberta.ca
console.log('MapleWay content script loaded');

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'scrapeData') {
    try {
      const data = scrapeAAIPData(request.selectedStream);
      sendResponse({ success: true, data: data });
    } catch (error) {
      sendResponse({ success: false, error: error.message });
    }
  }
  return true; // Keep the message channel open for async response
});

/**
 * Main scraping function
 */
function scrapeAAIPData(selectedStream) {
  const result = {
    summary2025: '',
    summary2026: {},
    eoiPool: [],
    drawInfo: []
  };

  // 1. Scrape 2025 Summary
  result.summary2025 = scrape2025Summary();

  // 2. Scrape 2026 Summaries (General + Stream Specific)
  result.summary2026 = scrape2026Summary(selectedStream);

  // 3. Scrape EOI Pool (Table 8)
  result.eoiPool = scrapeEOIPool();

  // 4. Scrape Draw Information (Table 9)
  result.drawInfo = scrapeDrawInfo(selectedStream);

  return result;
}

/**
 * Scrape 2025 summary text
 */
function scrape2025Summary() {
  // Look for text containing "AAIP issued" and "nominations in 2025"
  // Find the SHORTEST element to avoid catching parent containers
  const elements = document.querySelectorAll('p, li, div');
  let bestMatchEl = null;
  let minLength = Infinity;

  // 1. Find the specific leaf node (bullet point)
  for (let el of elements) {
    const text = el.textContent.trim();
    if (text.includes('AAIP issued') && text.includes('2025')) {
      if (text.length < minLength) {
        minLength = text.length;
        bestMatchEl = el;
      }
    }
  }

  if (!bestMatchEl) return 'No 2025 summary found';

  // 2. Check if it's part of a list (UL) to capture full context
  if (bestMatchEl.parentElement && bestMatchEl.parentElement.tagName === 'UL') {
    const parentText = bestMatchEl.parentElement.innerText.trim();
    // Safety: Only use parent if it's not absolutely huge (avoid grabbing nav menus if structure changes)
    if (parentText.length < 2000) {
      return parentText;
    }
  }

  return bestMatchEl.textContent.trim();
}

/**
 * Scrape 2026 summary data
 * Returns object with 'general' (Table 1) and 'stream' (Specific Table) data
 */
function scrape2026Summary(selectedStream) {
  const summary = {
    general: null,
    stream: null
  };

  const tables = document.querySelectorAll('table');

  for (let table of tables) {
    const caption = table.querySelector('caption');
    const title = findTableTitle(table);

    // Check for General Table (Process summary totals)
    if ((caption && caption.textContent.toLowerCase().includes('process summary totals')) ||
      (title && title.toLowerCase().includes('process summary totals'))) {

      const rows = table.querySelectorAll('tbody tr');
      for (let row of rows) {
        const cells = row.querySelectorAll('td, th');

        // Robustness: Check if row has enough cells and looks like the 2026 row
        if (cells.length >= 4) {
          // Case 1: First cell is "2026"
          if (cells[0].textContent.trim().includes('202')) {
            summary.general = {
              allocation: cells[1]?.textContent.trim() || '',
              issued: cells[2]?.textContent.trim() || '',
              remaining: cells[3]?.textContent.trim() || '',
              processing: cells[4]?.textContent.trim() || ''
            };
          }
          // Case 2: Table might be just data without 'Amount' column if formatting differs
          else if (summary.general === null) {
            // Fallback: try capturing the first row if we are sure it is the table
            summary.general = {
              allocation: cells[0]?.textContent.trim() || '',
              issued: cells[1]?.textContent.trim() || '',
              remaining: cells[2]?.textContent.trim() || '',
              processing: cells[3]?.textContent.trim() || ''
            };
          }
        }
      }
    }

    // Check for Stream Specific Table
    if (selectedStream) {
      const streamName = selectedStream.split('(')[0].trim(); // Remove (AOS) part
      const hasStreamInContext = (text) => text && text.toLowerCase().includes(streamName.toLowerCase());

      if ((caption && hasStreamInContext(caption.textContent)) ||
        (title && hasStreamInContext(title))) {

        summary.stream = [];
        const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
        const rows = table.querySelectorAll('tbody tr');

        rows.forEach(row => {
          const rowData = {};
          const cells = row.querySelectorAll('td, th');
          cells.forEach((cell, idx) => {
            rowData[headers[idx] || `col${idx}`] = cell.textContent.trim();
          });
          summary.stream.push(rowData);
        });
      }
    }
  }

  return summary;
}

/**
 * Scrape EOI Pool table (Table 8)
 */
function scrapeEOIPool() {
  const eoiData = [];

  const tables = document.querySelectorAll('table');

  for (let table of tables) {
    const caption = table.querySelector('caption');
    const title = findTableTitle(table);

    // Looser matching for "Expression of interest"
    if ((caption && caption.textContent.toLowerCase().includes('expression of interest')) ||
      (title && title.toLowerCase().includes('expression of interest'))) {

      const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
      const rows = table.querySelectorAll('tbody tr');
      rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length > 0) {
          const rowData = {};
          cells.forEach((cell, index) => {
            rowData[headers[index] || `col${index}`] = cell.textContent.trim();
          });
          eoiData.push(rowData);
        }
      });
      break;
    }
  }

  return eoiData;
}

/**
 * Scrape Draw Information table (Table 9) and filter by stream
 */
function scrapeDrawInfo(selectedStream) {
  const drawData = [];
  const streamKeyword = selectedStream.split('(')[0].trim();

  const tables = document.querySelectorAll('table');

  for (let table of tables) {
    const caption = table.querySelector('caption');
    const title = findTableTitle(table);

    if ((caption && caption.textContent.toLowerCase().includes('draw information')) ||
      (title && title.toLowerCase().includes('draw information'))) {

      const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
      const rows = table.querySelectorAll('tbody tr');
      rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length > 0) {
          const rowData = {};
          let isMatch = false;

          cells.forEach((cell, index) => {
            const cellText = cell.textContent.trim();
            rowData[headers[index] || `col${index}`] = cellText;

            if (cellText.toLowerCase().includes(streamKeyword.toLowerCase())) {
              isMatch = true;
            }
          });

          if (isMatch) {
            drawData.push(rowData);
          }
        }
      });
      break;
    }
  }

  return drawData;
}

/**
 * Helper to find table title by looking at previous siblings of table or its wrappers
 * Robustly checks up to 3 levels of potential wrappers (divs)
 */
function findTableTitle(table) {
  let current = table;
  // Go up to 3 levels to find a wrapper
  for (let i = 0; i < 3; i++) {
    let prev = current.previousElementSibling;
    while (prev) {
      // Check if tag is Heading (H1-H6) or Paragraph (P) possibly containing title
      if (prev.tagName.match(/^(H[1-6]|P)$/)) {
        return prev.textContent.trim();
      }
      prev = prev.previousElementSibling;
    }
    current = current.parentElement;
    if (!current) break;
  }
  return null;
}
