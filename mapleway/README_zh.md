# MapleWay 🍁 | 枫径

[![版本](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/tancolo/AI_Agent_Projects)
[![许可证: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[**English**](./README.md) | [简体中文]

**MapleWay** 是一款为 **阿尔伯塔省优势移民计划 (AAIP)** 申请人量身定制的专业浏览器插件。它能够自动从阿尔伯塔省政府官网抓取并分析复杂的处理数据，为您提供关于提名配额、抽签历史和候选池统计的清晰、有条理的视图。

<video width="640" height="360" controls>
  <source src="../assets/demo_for_Mapleway.mp4" type="video/mp4">
  您的浏览器不支持 HTML5 视频标签。
</video>

---

## 🌟 核心功能

### 🔍 智能数据抓取
- **实时提取**：自动从 `alberta.ca` 抓取最新的处理进度数据。
- **历史对比**：获取 2025 年总结数据，并与当前的 2026 年数据进行对比。
- **深度分析**：详细解析“处理摘要总额”（配额总量、已发放、剩余名额及处理中数量）。

### 🎯 针对性类别洞察
- **精准过滤**：选择您的具体申请类别（如：阿省机遇类 AOS、乡村振兴类 Rural Renewal、旅游酒店类等），仅查看与您相关的核心指标。
- **详细指标**：查看每个通道的具体提名数量和处理状态。

### 📊 意向表达 (EOI) 与 抽签信息
- **EOI 候选池追踪**：轻松监控“意向表达”候选池统计数据（Table 8）。
- **抽签历史分析**：查看“抽签信息”（Table 9）并集成自动计算功能。
- **自动汇总**：针对所选类别，自动计算多次抽签的累计邀请人数，省去手动计算的烦恼。

---

## 🚀 快速入门

### 前置条件
- Google Chrome、Microsoft Edge 或任何基于 Chromium 的浏览器。

### 安装步骤
1. **下载**：克隆或下载此仓库到本地。
2. **开发者模式**：打开浏览器，访问 `chrome://extensions/`。在右上角开启 **开发者模式**。
3. **加载插件**：点击 **加载已解压的扩展程序**，选择本项目中的 `/codebase/VanillaJS` 目录。
4. **固定插件**：为了方便使用，建议将 MapleWay 插件固定到浏览器工具栏。

### 使用方法
1. 访问 [AAIP 处理信息官方页面](https://www.alberta.ca/aaip-processing-information)。
2. 点击浏览器工具栏中的 **MapleWay** 图标。
3. 在下拉菜单中选择您的移民类别。
4. 点击 **Analyze Page**（分析页面），即可查看结构化的数据报告。

---

## 📂 项目结构

- `codebase/VanillaJS/`：插件核心源代码 (Manifest V3)。
- `PRD/`：详细的产品需求文档和 UI 设计稿。
- `automated_test/`：用于验证数据抓取准确性的自动化测试脚本。
- `icon_utils/`：插件图标资源及处理脚本。
- `screenshots/`：功能演示截图和视觉指南。

---

## 🛠 技术栈
- **核心引擎**：原生 JavaScript (ES6+)
- **界面设计**：CSS3 (响应式布局与现代审美)
- **平台规范**：Chrome Extension Manifest V3
- **抓取技术**：DOM 解析与模式匹配

---

## 📝 路线图
- [x] v0.1：实现基础抓取、配额总结和 AOS 类别支持。
- [x] v0.2：增强 EOI 追踪功能及抽签邀请人数自动汇总。
- [ ] v0.3：UI 界面全面翻新，支持多页面数据抓取。
- [ ] 未来：引入数据可视化图表及云端同步映射。

---

## 📄 许可证
本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 🤝 贡献
欢迎提交贡献！如有任何建议或问题，请在 [Issues](./Issues) 目录中提交 Issue 或发起 Pull Request。

---

*注：本插件为第三方工具，不代表阿尔伯塔省政府官方，亦与其无隶属关系。*
