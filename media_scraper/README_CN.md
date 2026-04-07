# Media Scraper (教育学习媒体抓取项目 V0.3) 🎵

本项目是一个基于教育与研究目的的自动化媒体存档工具，通过 Google Antigravity AI 辅助开发。V0.3 版本已升级为支持批量配置化抓取和命令行直接下载的双模式工具。

## 📖 项目背景 (Project Purpose)
该项目专注于合规的媒体资源检索：
- **目标**: 通过配置文件定义抓取任务，自动化搜索并下载音频或视频资源；或通过命令行直接下载指定URL。
- **鲁棒性**: 具备完善的"回退机制"。下载失败（如版权限制、网络问题）的资源会自动记录链接至 Markdown 文件，确保数据不丢失。

## ✨ V0.3 核心特性

- **双模式运行**:
  - **配置模式**: 从 `scraper_config.ini` 批量处理多个歌手
  - **直接URL模式**: 下载浏览时发现的特定视频
- **多媒体支持**:
  - **Audio**: 支持 mp3 等格式，可指定码率 (如 320k)。
  - **Video**: 支持 webm/mp4，可指定分辨率 (如 1080p, 720p)。
- **智能分类**:
  - 配置下载: `downloads/{歌手名}/`
  - 直接下载: `downloads/Direct_Downloads/`
  - 失败链接: `markdown_links/{文件夹名}_Links.md`
- **质量控制**: 可设定音频码率或视频分辨率。

## 🛠️ 使用说明 (Usage)

### 环境准备
```powershell
# 安装核心依赖
pip install yt-dlp
# 安装 ffmpeg (媒体转换必备)
winget install --id Gyan.FFmpeg
```

### 配置模式 (批量处理)
修改 `scraper_config.ini` 文件:
```ini
[Artist:周杰伦]
keywords = Jay Chou Official, 周杰伦 官方MV
media_type = video
quality = 1080p
```

运行:
```powershell
python media_archiver.py
```

### 直接URL模式 (V0.3 新功能!)
下载单个URL:
```powershell
python media_archiver.py https://www.youtube.com/watch?v=...
```

下载多个URL:
```powershell
python media_archiver.py URL1 URL2 URL3
```

从文本文件批量下载 (每行一个URL):
```powershell
python media_archiver.py --list my_urls.txt
```

直接通过命令行动态指定格式与画质 (覆盖 .ini 配置):
```powershell
python media_archiver.py https://... --type audio --format mp3 --quality 0
# 可选参数范围:
# --type [audio|video]
# --format [mp4|mp3|webm|m4a|...]
# --quality [1080|720|0|320K|...]
```

### 输出位置
- **配置模式**: `./downloads/{歌手}/`
- **直接模式**: `./downloads/Direct_Downloads/`
- **日志**: `archiver_log.txt`
- **失败记录**: `./markdown_links/`

## 📂 项目结构
- `media_archiver.py`: 主程序入口 (支持CLI)。
- `scraper_config.ini`: 批量模式配置文件。
- `media_python/`: 核心代码逻辑包。
- `ayumi_hamasaki_archiver.py`: V0.1 旧版脚本（保留参考）。
- `debug/`: 调试和对比工具。

---
*注: 本项目及其脚本仅供教育学习研究使用，请在法律和各平台服务协议允许范围内使用。*
