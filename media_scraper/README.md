# Media Scraper 🎵

This project is an automated media archiving tool created for educational and research purposes, developed with the assistance of Google Antigravity AI. It aims to retrieve and organize audio/video resources from compliant, open web platforms (such as YouTube, SoundCloud, etc.).

[中文版 (Chinese Version)](./README_CN.md)

## 📖 Project Background
The project focuses on compliant media resource retrieval:
- **Objective**: Scrape publicly available audio content and convert it into desired formats (e.g., MP3).
- **Process**: Uses Python scripts to automate search, analysis, and download logic.
- **Robustness**: Features a comprehensive error-handling mechanism. If a download fails (due to large file size, website restrictions, or network issues), the script won't crash; instead, it logs the Song Title, Source URL, and Error Reason into a specific Markdown file.

## ✨ Key Features

- **Compliant Parsing**: Interacts with public media platforms using compliant open-source libraries like `yt-dlp`.
- **Multi-Format Support**: Supports audio extraction and saving as `.mp3` (with configurable quality).
- **Smart Fallback Logic**: 
  - On download failure, it automatically extracts **Song Title** + **Source URL** + **Reason**.
  - Appends this information to `Ayumi_Hamasaki_Links.md`.
- **Automatic Logging**: Generates `archiver_log.txt` to track every step of the execution.

## 🚀 Current Progress

Currently implemented a specialized archiver for **Ayumi Hamasaki (浜崎あゆみ)**: `ayumi_hamasaki_archiver.py`.
- ✅ Integrated YouTube Search.
- ✅ Local FFmpeg integration (auto-detected or manually configured).
- ✅ Successfully scraped and converted multiple official audio resources.

## 🗺️ Roadmap (Future Optimizations)

Plans to refactor the script into a more generic, configuration-driven tool:
- **Configuration-Driven**:
  - **Artist/Keywords**: Dynamically set search targets.
  - **Media Type**: Choose between Audio or Video.
  - **Download Format**: Support for `mp3`, `webm`, `mp4`, etc.
  - **Quality**: Allow setting bitrate or resolution (e.g., 320kbps, 1080p).

## 🛠️ Usage

1. **Prerequisites**:
   ```powershell
   # Install core dependencies
   pip install yt-dlp
   # Install FFmpeg (for format conversion)
   winget install --id Gyan.FFmpeg
   ```

2. **Run Script**:
   ```powershell
   python ayumi_hamasaki_archiver.py
   ```

3. **Check Results**:
   - Successful MP3s: `./downloads/ayumi_hamasaki/`
   - Failure records: `./Ayumi_Hamasaki_Links.md`

---
*Note: This project and its scripts are for educational research purposes only. Please use within the bounds of laws and platform terms of service.*
