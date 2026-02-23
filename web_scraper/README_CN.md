# Web Scraper V0.3 (网络爬虫)

[English Version (英文版本)](README.md)

## 项目概述
Web Scraper V0.3 是一个多平台自动化工具，旨在聚合多个技术博客平台（CSDN、简书、掘金）的文章元数据。该工具能够处理无限滚动、自动翻页、详情提取，并自动进行数据合并、去重、标题中英翻译，最终生成结构化的 Markdown 报告。

## 核心功能
- **多平台支持**：支持 CSDN、简书、掘金平台的数据抓取。
- **统一工作流**：通过单一入口脚本 (`main_scraper.py`) 运行整个流程。
- **健壮的数据处理**：支持跨平台去重及自动翻译功能。
- **IPv4 优化翻译**：通过强制 IPv4 绕过 IPv6 超时，大幅提升 Google 翻译速度。
- **进度实时提示**：终端显示倒计时进度 (`总数 - 已处理 = 剩余`)。
- **结构化输出**：生成规范的 CSV 数据和专业的 Markdown 报告。
- **配置驱动**：目标 URL 和输出目录均可通过外部 `config.json` 文件进行全面管理。
- **独立运行模式**：爬虫脚本现在支持在命令行独立运行和测试，同时依然能够读取主配置文件。

> [!NOTE]
> **V0.3 更新说明**：硬编码的平台 URL 已成功从 `scraper_core/` 目录的文件中移除。你现在可以在项目根目录的 `config.json` 文件中轻松定制配置或更改源 URL。

## 目录结构
- `config.json`：中央配置文件，提供平台 URL 和导出路径的映射。
- `main_scraper.py`：项目调度器，读取 `config.json` 并按顺序运行已启用的平台爬虫。
- `scraper_core/`：核心逻辑目录，包含各平台抓取及后端处理脚本。
  - `csdn_scraper.py`
  - `jianshu_scraper.py`
  - `juejin_scraper.py`
  - `merge_articles_data.py`：负责合并 CSV 并进行标题翻译。
  - `generate_final_md.py`：生成最终的 Markdown 报告。
- `scraper_output/`：产出物目录。
  - 各平台原始 CSV 文件。
  - `merged_articles_final.csv`：汇总去重后的数据库。
  - `final_articles_report.md`：最终生成的阅读报告。
- `scraper_debug/`：包含调试用的测试脚本和工具。

## 环境要求
- Python 3.8+
- Chromium 浏览器（通过 Playwright 安装）

## 安装步骤

1. 安装必要的 Python 库：
   ```bash
   pip install -r requirements.txt
   ```

2. 安装 Playwright 浏览器二进制文件：
   ```bash
   playwright install chromium
   ```

## 配置与使用

项目具有高度可配置性。打开根目录下的 `config.json` 即可设置 `"enabled": true/false`，配置数据源 `url`，并重命名输出文件。

### 管道串联执行
要运行所有已启用的爬虫，并随后执行去重和报告生成步骤：
```bash
python main_scraper.py
```

### 独立爬虫执行
如果仅想测试或抓取单个平台的数据：
```bash
python scraper_core/csdn_scraper.py
python scraper_core/jianshu_scraper.py
python scraper_core/juejin_scraper.py
```
各个脚本会自动解析 `config.json` 获取所需的参数。

### 脚本执行流程
1. **抓取阶段**：加载配置，按需调用三个平台的爬虫，浏览器会自动打开（非无头模式）。
2. **合并与翻译**：合并生成的 CSV 文件，根据标题去重，并利用 IPv4 补丁快速完成标题翻译。
3. **报告生成**：按分类/专栏对文章进行分组，并写入 Markdown 文件。

## 输出结果
所有结果均保存在 `scraper_output/` 文件夹中。最重要的输出是 `final_articles_report.md`，它包含了按英文分类整理的所有文章链接。
