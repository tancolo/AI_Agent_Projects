// Popup script for MapleWay extension
document.addEventListener('DOMContentLoaded', init);

let selectedStream = '';

function init() {
    // Get DOM elements
    const streamSelect = document.getElementById('stream-select');
    const scrapeBtn = document.getElementById('scrape-btn');

    // Event listeners
    streamSelect.addEventListener('change', (e) => {
        selectedStream = e.target.value;
    });

    scrapeBtn.addEventListener('click', handleScrape);
}

/**
 * Handle scrape button click
 */
async function handleScrape() {
    if (!selectedStream) {
        showError('Please select an immigration stream first.');
        return;
    }

    showLoading(true);
    hideError();
    hideResults();

    // Debug helper to update status (updates loading text if available)
    const updateStatus = (msg) => {
        const loadingText = document.querySelector('#loading p');
        if (loadingText) loadingText.textContent = msg;
        console.log(msg);
    };

    try {
        updateStatus('Connecting to page...');

        // Get the active tab
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        // Check if we're on the right domain
        if (!tab || !tab.url || !tab.url.includes('alberta.ca')) {
            throw new Error('Please navigate to an alberta.ca page first.');
        }

        let response;

        // Timeout wrapper
        const withTimeout = (promise, ms, name) => {
            return Promise.race([
                promise,
                new Promise((_, reject) => setTimeout(() => reject(new Error(`${name} timed out after ${ms}ms`)), ms))
            ]);
        };

        try {
            updateStatus('Sending request...');
            // Try to send message to existing content script (5s timeout)
            response = await withTimeout(
                chrome.tabs.sendMessage(tab.id, {
                    action: 'scrapeData',
                    selectedStream: selectedStream
                }),
                5000,
                'Initial connection'
            );
        } catch (msgError) {
            console.warn('Initial connection failed:', msgError);

            // If connection fails, inject script
            if (msgError.message.includes('Could not establish connection') ||
                msgError.message.includes('receiving end does not exist')) {

                updateStatus('Injecting script...');
                await withTimeout(
                    chrome.scripting.executeScript({
                        target: { tabId: tab.id },
                        files: ['scripts/content.js']
                    }),
                    5000,
                    'Script injection'
                );

                // Wait briefly for script to initialize
                await new Promise(resolve => setTimeout(resolve, 200));

                updateStatus('Retrying request...');
                response = await withTimeout(
                    chrome.tabs.sendMessage(tab.id, {
                        action: 'scrapeData',
                        selectedStream: selectedStream
                    }),
                    5000,
                    'Retry connection'
                );
            } else {
                throw msgError;
            }
        }

        updateStatus('Processing data...');
        if (response && response.success) {
            displayResults(response.data);
        } else {
            throw new Error(response ? response.error : 'Failed to scrape data');
        }
    } catch (error) {
        console.error('Scrape error:', error);
        showError(`${error.message}. Please refresh the page.`);
    } finally {
        showLoading(false);
    }
}

/**
 * Display scraped data
 */
function displayResults(data) {
    // Show results container
    document.getElementById('results').classList.remove('hidden');

    // Display 2025 Summary
    const summary2025El = document.getElementById('summary-2025');

    let summary2025Html = '<strong>2025 Summary:</strong>';

    if (data.summary2025) {
        // Check if plain text or needs formatting
        // If it comes from a list (contains newlines), render as list
        const lines = data.summary2025.split('\n').filter(line => line.trim().length > 0);

        if (lines.length > 1) {
            summary2025Html += '<ul style="margin-top: 5px; padding-left: 20px; text-align: left;">';
            lines.forEach(line => {
                // remove existing bullets if any to avoid double bullets
                const cleanLine = line.replace(/^[•o-]\s*/, '').trim();
                summary2025Html += `<li>${cleanLine}</li>`;
            });
            summary2025Html += '</ul>';
        } else {
            summary2025Html += `<p style="margin-top: 5px;">${data.summary2025}</p>`;
        }
    } else {
        summary2025Html += '<p><em>No 2025 data found</em></p>';
    }

    summary2025El.innerHTML = summary2025Html;

    // Display 2026 Summary (Container for General + Stream)
    const summary2026Container = document.getElementById('summary-2026-container');
    summary2026Container.innerHTML = '<strong>2026 Summary:</strong>';

    // 1. General 2026 Table
    if (data.summary2026 && data.summary2026.general && data.summary2026.general.allocation) {
        summary2026Container.innerHTML += `
         <div class="sub-section">
            <p><em>General Summary</em></p>
            <table>
                <thead>
                    <tr>
                        <th>Allocation</th>
                        <th>Issued</th>
                        <th>Remaining</th>
                        <th>Processing</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>${data.summary2026.general.allocation}</td>
                        <td>${data.summary2026.general.issued}</td>
                        <td>${data.summary2026.general.remaining}</td>
                        <td>${data.summary2026.general.processing}</td>
                    </tr>
                </tbody>
            </table>
         </div>
        `;
    } else {
        summary2026Container.innerHTML += '<p><em>No general 2026 data found</em></p>';
    }

    // 2. Stream Specific 2026 Table
    if (data.summary2026 && data.summary2026.stream && data.summary2026.stream.length > 0) {
        summary2026Container.innerHTML += `
         <div class="sub-section" style="margin-top: 15px;">
            <p><em>${selectedStream} Allocation</em></p>
            ${createTable(data.summary2026.stream)}
         </div>
        `;
    }

    // Display Worker Expression Of Interest (EOI Pool) - Full Table
    if (data.eoiPool && data.eoiPool.length > 0) {
        const eoiSection = document.getElementById('eoi-section');
        const eoiTableEl = document.getElementById('eoi-table');

        eoiSection.classList.remove('hidden');
        eoiTableEl.innerHTML = createTable(data.eoiPool);
    }

    // Display Draw Information Table with Totals
    if (data.drawInfo && data.drawInfo.length > 0) {
        const drawSection = document.getElementById('draw-section');
        const drawTableEl = document.getElementById('draw-table');

        drawSection.classList.remove('hidden');

        // Calculate total invitations
        const totalInvitations = calculateTotalInvitations(data.drawInfo);

        // Add total row
        const dataWithTotal = [...data.drawInfo];
        if (totalInvitations > 0) {
            dataWithTotal.push({
                'Draw date': 'NA',
                'Worker stream, pathway, initiative or other focus and selection parameters': 'Total',
                'Minimum score of invited candidates': 'NA',
                'Number of invitations': totalInvitations.toString()
            });
        }

        drawTableEl.innerHTML = createTable(dataWithTotal, true);
    }
}

/**
 * Create HTML table from data array
 */
function createTable(dataArray, highlightTotal = false) {
    if (!dataArray || dataArray.length === 0) {
        return '<p><em>No data available</em></p>';
    }

    // Get headers from first object
    const headers = Object.keys(dataArray[0]);

    let html = '<table><thead><tr>';
    headers.forEach(header => {
        html += `<th>${header}</th>`;
    });
    html += '</tr></thead><tbody>';

    // Add data rows
    dataArray.forEach((row, index) => {
        const isLastRow = index === dataArray.length - 1;
        const rowClass = (highlightTotal && isLastRow) ? ' class="total-row"' : '';

        html += `<tr${rowClass}>`;
        headers.forEach(header => {
            html += `<td>${row[header] || ''}</td>`;
        });
        html += '</tr>';
    });

    html += '</tbody></table>';
    return html;
}

/**
 * Calculate total invitations from draw data
 */
function calculateTotalInvitations(drawData) {
    let total = 0;

    drawData.forEach(row => {
        // Look for "Number of invitations" column
        const invitations = row['Number of invitations'] || row['number of invitations'];
        if (invitations) {
            // Remove commas and parse as integer
            const num = parseInt(invitations.replace(/,/g, ''));
            if (!isNaN(num)) {
                total += num;
            }
        }
    });

    return total;
}

/**
 * Show/hide loading indicator
 */
function showLoading(show) {
    const loadingEl = document.getElementById('loading');
    const scrapeBtn = document.getElementById('scrape-btn');

    if (show) {
        loadingEl.classList.remove('hidden');
        scrapeBtn.disabled = true;
    } else {
        loadingEl.classList.add('hidden');
        scrapeBtn.disabled = false;
    }
}

/**
 * Show error message
 */
function showError(message) {
    const errorEl = document.getElementById('error');
    errorEl.textContent = message;
    errorEl.classList.remove('hidden');
}

/**
 * Hide error message
 */
function hideError() {
    document.getElementById('error').classList.add('hidden');
}

/**
 * Hide results
 */
function hideResults() {
    document.getElementById('results').classList.add('hidden');
    document.getElementById('eoi-section').classList.add('hidden');
    document.getElementById('draw-section').classList.add('hidden');
}
