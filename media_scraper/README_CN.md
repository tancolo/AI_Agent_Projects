# Media Scraper (教育学习媒体抓取项目) 🎵

本项目是一个基于教育与研究目的的自动化媒体存档工具，通过 Google Antigravity AI 辅助开发。它旨在从合规的开放网络平台（如 YouTube/SoundCloud 等）检索并整理音频/视频资源。

## 📖 项目背景 (Project Purpose)
该项目专注于合规的媒体资源检索：
- **目标**: 抓取公开发布的音频内容并转换为高质量格式（如 MP3）。
- **流程**: 使用 Python 脚本自动化搜索、分析及下载逻辑。
- **鲁棒性**: 具备完善的错误处理机制。如果下载因各种原因（如文件过大、网站限制或网络波动）失败，脚本不会异常终止，而是将相关信息记录在 MD 文件中。

## ✨ 核心功能 (Key Features)

- **合法解析**: 使用 `yt-dlp` 等合规开源库对接公开发布的媒体平台。
- **多格式支持**: 支持提取音频并保存为 `.mp3` 等格式（可配置质量）。
- **智能回退逻辑 (Fallback)**: 
  - 下载失败时，自动提取 **歌曲名称 (Title)** + **原始链接 (URL)** + **失败原因 (Reason)**。
  - 将上述信息追加保存至 `Ayumi_Hamasaki_Links.md`。
- **自动日志管理**: 生成 `archiver_log.txt` 记录每一步执行详情。

## 🚀 当前进度 (Current Status)

目前已实现针对歌手 **Ayumi Hamasaki (浜崎あゆみ)** 的专项抓取脚本 `ayumi_hamasaki_archiver.py`。
- ✅ 成功对接 YouTube Search。
- ✅ 实现 ffmpeg 本地集成（自动通过 Winget 或手动配置路径）。
- ✅ 成功抓取并转换多首官方音频资源。

## 🗺️ 未来优化路线 (Roadmap)

计划将脚本重构为更加通用的配置化工具：
- **配置化驱动 (Config-based)**:
  - **歌手/关键词**: 动态设定搜索目标。
  - **媒体类型**: 支持 音频 (Audio) 或 视频 (Video) 的选择。
  - **下载格式**: 支持 `mp3`, `webm`, `mp4` 等多种封装格式。
  - **下载质量**: 允许设定码率或分辨率（如 320kbps, 1080p 等）。

## 🛠️ 使用说明 (Usage)

1. **环境准备**:
   ```powershell
   # 安装核心依赖
   pip install yt-dlp
   # 安装 ffmpeg (用于格式转换)
   winget install --id Gyan.FFmpeg
   ```

2. **运行脚本**:
   ```powershell
   python ayumi_hamasaki_archiver.py
   ```

3. **查看结果**:
   - 下载成功的 MP3: `./downloads/ayumi_hamasaki/`
   - 无法下载的记录: `./Ayumi_Hamasaki_Links.md`

---
*注: 本项目及其脚本仅供教育学习研究使用，请在法律和各平台服务协议允许范围内使用。*
