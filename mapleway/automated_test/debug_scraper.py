from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

def main():
    print("🚀 Starting MapleWay Debug Scraper...")
    
    # 1. Setup Chrome Driver
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Uncomment to run headless
    
    print("🌍 Launching Chrome and navigating to Alberta AAIP page...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # 2. Navigate to URL
        url = "https://www.alberta.ca/aaip-processing-information"
        driver.get(url)
        time.sleep(5) # Wait for page to fully load
        
        print("✅ Page loaded.")
        print("💉 Injecting scraping logic...")
        
        # 3. Inject JS Logic (The exact logic from content.js)
        # We wrap it in a function and call it immediately
        js_logic = """
        return (function() {
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

            // ... Helper functions definitions ... 
            
            function scrape2025Summary() {
              // Find SHORTEST match to avoid container divs
              const elements = document.querySelectorAll('p, li, div');
              let bestMatch = null;
              let minLength = Infinity;

              for (let el of elements) {
                const text = el.textContent.trim();
                if (text.includes('AAIP issued') && text.includes('2025')) {
                  if (text.length < minLength) {
                    minLength = text.length;
                    bestMatch = text;
                  }
                }
              }
              return bestMatch || 'No 2025 summary found';
            }

            function scrape2026Summary(selectedStream) {
              const summary = { general: null, stream: null };
              const tables = document.querySelectorAll('table');

              for (let table of tables) {
                const caption = table.querySelector('caption');
                const title = findTableTitle(table);
                
                if ((caption && caption.textContent.toLowerCase().includes('process summary totals')) ||
                    (title && title.toLowerCase().includes('process summary totals'))) {
                  
                  const rows = table.querySelectorAll('tbody tr');
                  for (let row of rows) {
                    const cells = row.querySelectorAll('td, th');
                    if (cells.length >= 4) {
                         if (cells[0].textContent.trim().includes('202')) {
                            summary.general = {
                                allocation: cells[1]?.textContent.trim() || '',
                                issued: cells[2]?.textContent.trim() || '',
                                remaining: cells[3]?.textContent.trim() || '',
                                processing: cells[4]?.textContent.trim() || ''
                            };
                         } else if (summary.general === null) {
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

                if (selectedStream) {
                  const streamName = selectedStream.split('(')[0].trim();
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

            function scrapeEOIPool() {
              const eoiData = [];
              const tables = document.querySelectorAll('table');
              for (let table of tables) {
                const caption = table.querySelector('caption');
                const title = findTableTitle(table);
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

            function findTableTitle(table) {
              let current = table;
              for (let i = 0; i < 3; i++) {
                let prev = current.previousElementSibling;
                while (prev) {
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

            return scrapeAAIPData('Alberta Opportunity Stream (AOS)');
        })();
        """
        
        result = driver.execute_script(js_logic)
        
        print("\n📊 SCRAPING RESULTS:\n")
        print(json.dumps(result, indent=2))
        
        print("\n✅ Verification Complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("Closing browser in 10 seconds...")
        time.sleep(10)
        driver.quit()

if __name__ == "__main__":
    main()
