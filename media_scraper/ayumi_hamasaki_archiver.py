#!/usr/bin/env python3
"""
Ayumi Hamasaki Audio Archiver
=============================
Educational research script to find and archive audio content for Ayumi Hamasaki (浜崎あゆみ)
using legal sources (YouTube via yt-dlp).

Requirements:
    pip install yt-dlp

Usage:
    python ayumi_hamasaki_archiver.py

Author: Educational Research Script
License: For educational/research purposes only
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# ============================================================================
# CONFIGURATION
# ============================================================================

# Search query for finding content
ARTIST_NAME = "Ayumi Hamasaki"
ARTIST_NAME_JP = "浜崎あゆみ"
SEARCH_QUERIES = [
    f"{ARTIST_NAME} official audio",
    f"{ARTIST_NAME} official music video",
    f"{ARTIST_NAME_JP} official",
]

# Maximum number of results to fetch per query
MAX_RESULTS_PER_QUERY = 5

# Output directories and files
OUTPUT_DIR = Path("./downloads/ayumi_hamasaki")
LINKS_FILE = Path("./Ayumi_Hamasaki_Links.md")
LOG_FILE = Path("./archiver_log.txt")

# Audio quality settings
AUDIO_FORMAT = "mp3"
AUDIO_QUALITY = "0"  # Best quality (0 = best, 9 = worst for mp3)

# FFmpeg location (set to None to use system PATH, or specify explicit path)
# Windows example: r"C:\Users\John Tan\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
FFMPEG_LOCATION = r"C:\Users\John Tan\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def log_message(message: str, level: str = "INFO") -> None:
    """Log a message to console and log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")


def ensure_directories() -> None:
    """Create necessary directories if they don't exist."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    log_message(f"Output directory ensured: {OUTPUT_DIR.absolute()}")


def check_yt_dlp_installed() -> bool:
    """Check if yt-dlp is installed and accessible."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            log_message(f"yt-dlp version: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        log_message("yt-dlp not found. Please install it with: pip install yt-dlp", "ERROR")
    except subprocess.TimeoutExpired:
        log_message("yt-dlp check timed out", "ERROR")
    except Exception as e:
        log_message(f"Error checking yt-dlp: {e}", "ERROR")
    return False


def initialize_links_file() -> None:
    """Initialize or update the links markdown file with a header."""
    header = f"""# Ayumi Hamasaki (浜崎あゆみ) - Audio Archive Links

> **Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
> **Purpose:** Educational research - archiving publicly available content

---

## Contents

This file contains links to audio content that could not be directly downloaded.
Each entry includes the song title and source URL for manual access.

---

## Links

"""
    if not LINKS_FILE.exists():
        with open(LINKS_FILE, "w", encoding="utf-8") as f:
            f.write(header)
        log_message(f"Created links file: {LINKS_FILE.absolute()}")


def append_to_links_file(title: str, url: str, reason: str = "Download restricted") -> None:
    """Append a song entry to the links markdown file."""
    entry = f"""### {title}
- **URL:** [{url}]({url})
- **Reason:** {reason}
- **Added:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

"""
    with open(LINKS_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
    log_message(f"Added to links file: {title}")


# ============================================================================
# SEARCH FUNCTIONS
# ============================================================================

def search_youtube(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search YouTube for videos matching the query.
    Returns a list of video metadata dictionaries.
    """
    log_message(f"Searching YouTube for: {query}")
    
    try:
        # Use yt-dlp to search YouTube
        search_url = f"ytsearch{max_results}:{query}"
        
        result = subprocess.run(
            [
                sys.executable, "-m", "yt_dlp",
                "--dump-json",           # Output video info as JSON
                "--flat-playlist",       # Don't download, just get info
                "--no-warnings",         # Suppress warnings
                search_url
            ],
            capture_output=True,
            text=True,
            timeout=60,
            encoding="utf-8"
        )
        
        videos = []
        if result.stdout:
            # Each line is a JSON object for one video
            for line in result.stdout.strip().split("\n"):
                if line:
                    try:
                        video_info = json.loads(line)
                        videos.append({
                            "id": video_info.get("id", ""),
                            "title": video_info.get("title", "Unknown Title"),
                            "url": video_info.get("url") or f"https://www.youtube.com/watch?v={video_info.get('id', '')}",
                            "duration": video_info.get("duration", 0),
                            "uploader": video_info.get("uploader", "Unknown"),
                            "view_count": video_info.get("view_count", 0),
                        })
                    except json.JSONDecodeError:
                        continue
        
        log_message(f"Found {len(videos)} videos for query: {query}")
        return videos
        
    except subprocess.TimeoutExpired:
        log_message(f"Search timed out for: {query}", "WARNING")
    except Exception as e:
        log_message(f"Search error: {e}", "ERROR")
    
    return []


# ============================================================================
# DOWNLOAD FUNCTIONS
# ============================================================================

def download_audio(video_url: str, title: str) -> bool:
    """
    Attempt to download audio from a video URL and convert to MP3.
    Returns True if successful, False otherwise.
    """
    log_message(f"Attempting to download: {title}")
    
    # Sanitize filename
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_', '.')).strip()
    safe_title = safe_title[:100]  # Limit filename length
    
    output_template = str(OUTPUT_DIR / f"{safe_title}.%(ext)s")
    
    try:
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--extract-audio",                    # Extract audio only
            "--audio-format", AUDIO_FORMAT,       # Convert to MP3
            "--audio-quality", AUDIO_QUALITY,     # Best quality
            "--embed-thumbnail",                  # Embed thumbnail if available
            "--add-metadata",                     # Add metadata
            "--no-playlist",                      # Don't download playlists
            "--output", output_template,          # Output filename template
            "--no-warnings",                      # Suppress warnings
            "--progress",                         # Show progress
        ]
        
        # Add ffmpeg location if specified
        if FFMPEG_LOCATION:
            cmd.extend(["--ffmpeg-location", FFMPEG_LOCATION])
        
        cmd.append(video_url)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            encoding="utf-8"
        )
        
        if result.returncode == 0:
            log_message(f"Successfully downloaded: {title}", "SUCCESS")
            return True
        else:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            log_message(f"Download failed for {title}: {error_msg}", "WARNING")
            return False
            
    except subprocess.TimeoutExpired:
        log_message(f"Download timed out for: {title}", "WARNING")
    except Exception as e:
        log_message(f"Download error for {title}: {e}", "ERROR")
    
    return False


# ============================================================================
# MAIN ARCHIVER LOGIC
# ============================================================================

def archive_content() -> Dict[str, int]:
    """
    Main function to search for and archive Ayumi Hamasaki content.
    Returns statistics about the operation.
    """
    stats = {
        "searched": 0,
        "found": 0,
        "downloaded": 0,
        "linked": 0,
        "failed": 0
    }
    
    # Track URLs to avoid duplicates
    processed_urls = set()
    
    for query in SEARCH_QUERIES:
        stats["searched"] += 1
        videos = search_youtube(query, MAX_RESULTS_PER_QUERY)
        
        for video in videos:
            video_url = video["url"]
            title = video["title"]
            
            # Skip duplicates
            if video_url in processed_urls:
                log_message(f"Skipping duplicate: {title}")
                continue
            
            processed_urls.add(video_url)
            stats["found"] += 1
            
            # Attempt download
            if download_audio(video_url, title):
                stats["downloaded"] += 1
            else:
                # Fallback: Save to links file
                append_to_links_file(
                    title=title,
                    url=video_url,
                    reason="Download restricted or failed"
                )
                stats["linked"] += 1
    
    return stats


def print_summary(stats: Dict[str, int]) -> None:
    """Print a summary of the archiving operation."""
    summary = f"""
╔════════════════════════════════════════════════════════════════╗
║           AYUMI HAMASAKI AUDIO ARCHIVER - SUMMARY              ║
╠════════════════════════════════════════════════════════════════╣
║  Queries executed:     {stats['searched']:>5}                                   ║
║  Videos found:         {stats['found']:>5}                                   ║
║  Successfully downloaded: {stats['downloaded']:>5}                                ║
║  Saved to links file:  {stats['linked']:>5}                                   ║
╠════════════════════════════════════════════════════════════════╣
║  Output directory: {str(OUTPUT_DIR.absolute()):<40} ║
║  Links file: {str(LINKS_FILE.absolute()):<47} ║
╚════════════════════════════════════════════════════════════════╝
"""
    print(summary)
    log_message("Archiving operation completed")


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the archiver script."""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║     AYUMI HAMASAKI (浜崎あゆみ) AUDIO ARCHIVER                ║
    ║     Educational Research Tool                                 ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize
    ensure_directories()
    initialize_links_file()
    
    # Check dependencies
    if not check_yt_dlp_installed():
        print("\n❌ yt-dlp is required but not installed.")
        print("   Install it with: pip install yt-dlp")
        sys.exit(1)
    
    # Run the archiver
    log_message("Starting audio archiver...")
    stats = archive_content()
    
    # Print summary
    print_summary(stats)
    
    print("\n✅ Archiving complete!")
    print(f"   • Downloaded files: {OUTPUT_DIR.absolute()}")
    print(f"   • Links file: {LINKS_FILE.absolute()}")
    print(f"   • Log file: {LOG_FILE.absolute()}")


if __name__ == "__main__":
    main()
