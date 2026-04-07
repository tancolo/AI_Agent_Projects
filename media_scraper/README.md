# Media Scraper (V0.3) 🎵

This project is an automated media archiving tool created for educational and research purposes, developed with the assistance of Google Antigravity AI. It acts as a configuration-driven downloader for retrieving compliant media from open platforms, with support for both batch processing and ad-hoc direct URL downloads.

[中文版 (Chinese Version)](./README_CN.md)

## 📖 Project Purpose
- **Objective**: Archive publicly available Audio/Video content from platforms like YouTube based on a customizable configuration OR download specific URLs directly via command line.
- **Robustness**: Features specialized error handling. Failed downloads are not lost but logged into Markdown files for manual review.

## ✨ Key Features (V0.3)

- **Dual Mode Operation**:
  - **Config Mode**: Batch process multiple artists from `scraper_config.ini`
  - **Direct URL Mode**: Download specific videos you find while browsing
- **Multi-Format**: Supports **Audio** (mp3, etc.) and **Video** (mp4, webm, etc.).
- **Smart Organization**:
  - Config downloads: `downloads/{Artist Name}/`
  - Direct downloads: `downloads/Direct_Downloads/`
  - Failed links: `markdown_links/{Folder_Name}_Links.md`
- **Quality Control**: Set specific bitrate for audio or resolution (e.g., 1080p, 720p) for video.

## 🛠️ Usage

### Prerequisites
```powershell
pip install yt-dlp
winget install --id Gyan.FFmpeg
```

### Config Mode (Batch Processing)
Edit `scraper_config.ini` to add your targets:
```ini
[Artist:My Favorite Band]
keywords = Band Name official video
media_type = video
quality = 1080p
```

Run:
```powershell
python media_archiver.py
```

### Direct URL Mode (V0.3 New!)
Download a single URL:
```powershell
python media_archiver.py https://www.youtube.com/watch?v=...
```

Download multiple URLs:
```powershell
python media_archiver.py URL1 URL2 URL3
```

Download from a text file (one URL per line):
```powershell
python media_archiver.py --list my_urls.txt
```

Override parameters dynamically for direct URLs or lists:
```powershell
python media_archiver.py https://www.youtube.com/watch?v=... --type audio --format mp3 --quality 0
# Options:
# --type [audio|video]
# --format [mp4|mp3|webm|m4a|...]
# --quality [1080|720|0|320K|...]
```

### Output Locations
- **Config Mode**: `./downloads/{Artist}/`
- **Direct Mode**: `./downloads/Direct_Downloads/`
- **Logs**: `archiver_log.txt`
- **Fallback Links**: `./markdown_links/`

## 📂 Project Structure
- `media_archiver.py`: Main entry point with CLI support.
- `scraper_config.ini`: Configuration file for batch mode.
- `media_python/`: Core logic modules.
- `ayumi_hamasaki_archiver.py`: Legacy script (V0.1).
- `debug/`: Debugging and comparison tools.

---
*Note: This project and its scripts are for educational research purposes only. Please use within the bounds of laws and platform terms of service.*
