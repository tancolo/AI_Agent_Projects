# Media Scraper (V0.2) 🎵

This project is an automated media archiving tool created for educational and research purposes, developed with the assistance of Google Antigravity AI. It acts as a configuration-driven downloader for retrieving compliant media from open platforms.

[中文版 (Chinese Version)](./README_CN.md)

## 📖 Project Purpose
- **Objective**: Archive publicly available Audio/Video content from platforms like YouTube based on a customizable configuration.
- **Robustness**: Features specialized error handling. Failed downloads are not lost but logged into Markdown files for manual review.

## ✨ Key Features (V0.2)

- **Config-Driven**: Define artists, media types, and quality settings in `scraper_config.ini`.
- **Multi-Format**: Supports **Audio** (mp3, etc.) and **Video** (mp4, webm, etc.).
- **Smart Organization**:
  - Downloads are automatically sorted into `downloads/{Artist Name}/`.
  - Failed links are tracked in `markdown_links/{Artist_Name}_Links.md`.
- **Quality Control**: Set specific bitrate for audio or resolution (e.g., 1080p, 720p) for video.

## 🛠️ Usage

1. **Prerequisites**:
   ```powershell
   pip install yt-dlp
   winget install --id Gyan.FFmpeg
   ```

2. **Configuration**:
   Edit `scraper_config.ini` to add your targets:
   ```ini
   [Artist:My Favorite Band]
   keywords = Band Name official video
   media_type = video
   quality = 1080p
   ```

3. **Run Script**:
   ```powershell
   python media_archiver.py
   ```

4. **Output**:
   - **Media**: `./downloads/`
   - **Logs**: `archiver_log.txt`
   - **Fallback Links**: `./markdown_links/`

## 📂 Project Structure
- `media_archiver.py`: Main entry point.
- `scraper_config.ini`: Configuration file.
- `media_python/`: Core logic modules.
- `ayumi_hamasaki_archiver.py`: Legacy script (V0.1).

---
*Note: This project and its scripts are for educational research purposes only. Please use within the bounds of laws and platform terms of service.*
