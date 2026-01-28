/**
 * Download Manager for MapleWay Extension
 * Handles UI injection and interaction for the download feature
 */

const DownloadManager = {
    currentStream: '',

    /**
     * Initialize the Download Manager
     * Fetches UI and injects it into the DOM
     */
    init: async function () {
        try {
            // Fetch the HTML template
            const response = await fetch('../download/download.html');
            if (!response.ok) throw new Error('Failed to load download UI');

            const html = await response.text();

            // Create styling link
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = '../download/download.css';
            document.head.appendChild(link);

            // Inject into results container
            const resultsContainer = document.getElementById('results');
            if (resultsContainer) {
                // Remove existing if any (dev hmr style safety)
                const existing = document.getElementById('download-section');
                if (existing) existing.remove();

                // Append html
                // We use a temp div to parse
                const temp = document.createElement('div');
                temp.innerHTML = html;
                const section = temp.firstElementChild;

                // Initially hidden until data is available
                section.classList.add('hidden');

                resultsContainer.appendChild(section);

                this.attachListeners();
            }
        } catch (error) {
            console.error('DownloadManager init error:', error);
        }
    },

    /**
     * Attach event listeners to buttons
     */
    attachListeners: function () {
        const btnPdf = document.getElementById('btn-pdf');

        if (btnPdf) {
            btnPdf.addEventListener('click', () => {
                this.handleDownload('pdf', btnPdf);
            });
        }

        // Word and Excel are disabled for now, but listeners could go here
    },

    /**
     * Handle download action
     */
    handleDownload: function (type, btnElement) {
        if (!this.currentStream) return;

        if (type === 'pdf') {
            // UI Feedback
            const originalText = btnElement.textContent;
            btnElement.textContent = 'Generating...';
            btnElement.disabled = true;

            // Call Generator
            if (typeof PDFGenerator !== 'undefined') {
                PDFGenerator.generate(this.currentStream)
                    .then(() => {
                        // Success
                        btnElement.textContent = 'Done!';
                        setTimeout(() => {
                            btnElement.textContent = originalText;
                            btnElement.disabled = false;
                        }, 2000);
                    })
                    .catch(err => {
                        console.error(err);
                        btnElement.textContent = 'Error';
                        setTimeout(() => {
                            btnElement.textContent = originalText;
                            btnElement.disabled = false;
                        }, 2000);
                    });
            } else {
                console.error('PDFGenerator not loaded');
                btnElement.textContent = 'Error';
                btnElement.disabled = false;
            }
        }
    },

    /**
     * Update state based on results
     * @param {boolean} show - Whether to show the download section
     * @param {string} streamName - The current stream name
     */
    updateState: function (show, streamName) {
        this.currentStream = streamName;
        const section = document.getElementById('download-section');

        if (section) {
            if (show) {
                section.classList.remove('hidden');
            } else {
                section.classList.add('hidden');
            }
        }
    }
};
