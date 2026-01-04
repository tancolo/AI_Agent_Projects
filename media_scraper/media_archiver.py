#!/usr/bin/env python3
"""
Media Scraper V0.2
==================
Generic, configuration-driven media archiver for educational research.
Reads from scraper_config.ini to download content for multiple artists.
"""

import sys
from media_python.config_loader import ConfigLoader
from media_python.scraper_core import MediaScraper
from media_python.utils import log_message

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                 MEDIA SCRAPER ARCHIVER V0.2                   ║
    ║                 Educational Research Tool                     ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Load Configuration
        loader = ConfigLoader("scraper_config.ini")
        config = loader.load()
        
        # Initialize Scraper
        scraper = MediaScraper(config)
        
        # Run
        log_message("Starting archiving process...", "INFO")
        scraper.run()
        log_message("Archiving process completed.", "SUCCESS")
        
    except FileNotFoundError as e:
        print(f"\n❌ Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        log_message(f"Crucial error: {e}", "CRITICAL")
        sys.exit(1)

if __name__ == "__main__":
    main()
