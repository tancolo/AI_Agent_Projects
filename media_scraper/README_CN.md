# Media Scraper (教育学习媒体抓取项目 V0.2) 🎵

本项目是一个基于教育与研究目的的自动化媒体存档工具，通过 Google Antigravity AI 辅助开发。V0.2 版本已升级为通用的配置化工具，支持多歌手、多格式的批量抓取。

## 📖 项目背景 (Project Purpose)
该项目专注于合规的媒体资源检索：
- **目标**: 通过配置文件定义抓取任务，自动化搜索并下载音频或视频资源。
- **鲁棒性**: 具备完善的“回退机制”。下载失败（如版权限制、网络问题）的资源会自动记录链接至 Markdown 文件，确保数据不丢失。

## ✨ V0.2 核心特性

- **配置化驱动 (Config-Based)**: 使用 `scraper_config.ini` 轻松管理抓取目标。
  - **动态搜索**: 支持自定义每个歌手的搜索关键词。
  - **显式分类**: 下载内容自动存入 `downloads/{歌手名}/` 文件夹。
- **多媒体支持**:
  - **Audio**: 支持 mp3 等格式，可指定码率 (如 320k)。
  - **Video**: 支持 webm/mp4，可指定分辨率 (如 1080p, 720p)。
- **智能日志与回退**:
  - 失败链接自动保存至 `markdown_links/{歌手名}_Links.md`。
  - 全程日志记录于 `archiver_log.txt`。

## 🛠️ 使用说明 (Usage)

1. **环境准备**:
   ```powershell
   # 安装核心依赖
   pip install yt-dlp
   # 安装 ffmpeg (媒体转换必备)
   winget install --id Gyan.FFmpeg
   ```

2. **配置任务**:
   修改 `scraper_config.ini` 文件:
   ```ini
   [Artist:周杰伦]
   keywords = Bay Jue Official, 周杰伦 官方MV
   media_type = video
   quality = 1080p
   
   [Artist:Adele]
   media_type = audio
   format = mp3
   ```

3. **运行脚本**:
   ```powershell
   python media_archiver.py
   ```

4. **查看结果**:
   - **媒体文件**: `./downloads/`
   - **失败记录**: `./markdown_links/`

## 📂 项目结构
- `media_archiver.py`: 主程序入口。
- `scraper_config.ini`: 配置文件。
- `media_python/`: 核心代码逻辑包。
- `ayumi_hamasaki_archiver.py`: V0.1 旧版脚本（保留参考）。

---
*注: 本项目及其脚本仅供教育学习研究使用，请在法律和各平台服务协议允许范围内使用。*
