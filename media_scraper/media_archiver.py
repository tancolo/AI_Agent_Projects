#!/usr/bin/env python3
"""
Media Scraper V0.3
==================
Generic, configuration-driven media archiver for educational research.
Supports both config-based batch processing and direct URL downloads via CLI.

Usage:
  Config mode:  python media_archiver.py
  Direct URL:   python media_archiver.py https://youtube.com/...
  Multiple:     python media_archiver.py URL1 URL2 URL3
  From file:    python media_archiver.py --list urls.txt
"""

import sys
import argparse
from pathlib import Path
from media_python.config_loader import ConfigLoader
from media_python.scraper_core import MediaScraper
from media_python.utils import log_message

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                 MEDIA SCRAPER ARCHIVER V0.3                   ║
    ║                 Educational Research Tool                     ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Media Scraper - Download media from YouTube and other platforms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Config mode:     python media_archiver.py
  Single URL:      python media_archiver.py https://youtube.com/watch?v=...
  Multiple URLs:   python media_archiver.py URL1 URL2 URL3
  From file:       python media_archiver.py --list my_urls.txt
        """
    )
    
    parser.add_argument(
        'urls',
        nargs='*',
        help='One or more URLs to download directly'
    )
    
    parser.add_argument(
        '--list',
        type=str,
        metavar='FILE',
        help='Path to a text file containing URLs (one per line)'
    )
    
    parser.add_argument('--type', choices=['audio', 'video'], help='Override media type (audio or video)')
    parser.add_argument('--format', type=str, help='Override output format (e.g., mp3, mp4, webm)')
    parser.add_argument('--quality', type=str, help='Override quality (e.g., 1080, 720, 0, 320K)')
    
    args = parser.parse_args()
    
    try:
        # Load Configuration
        loader = ConfigLoader("scraper_config.ini")
        config = loader.load()
        
        # Initialize Scraper
        scraper = MediaScraper(config)
        
        # Determine mode: Direct URL(s) or Config-based
        direct_urls = []
        
        # Collect URLs from command line args
        if args.urls:
            direct_urls.extend(args.urls)
        
        # Collect URLs from file
        if args.list:
            list_file = Path(args.list)
            if not list_file.exists():
                print(f"\n❌ Error: File not found: {args.list}")
                sys.exit(1)
            
            with open(list_file, 'r', encoding='utf-8') as f:
                for line in f:
                    url = line.strip()
                    if url and not url.startswith('#'):  # Skip empty lines and comments
                        direct_urls.append(url)
        
        # Execute based on mode
        if direct_urls:
            # Direct URL mode
            log_message(f"Direct download mode: {len(direct_urls)} URL(s)", "INFO")
            success_count = 0
            
            for url in direct_urls:
                if scraper.download_direct(url, media_type=args.type, fmt=args.format, quality=args.quality):
                    success_count += 1
            
            log_message(f"Direct downloads completed: {success_count}/{len(direct_urls)} successful", "SUCCESS")
            print(f"\n✅ Downloaded {success_count} out of {len(direct_urls)} URLs")
            print(f"   • Files saved to: downloads/Direct_Downloads/")
            
        else:
            # Config mode (default V0.2 behavior)
            log_message("Config-based archiving mode", "INFO")
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
