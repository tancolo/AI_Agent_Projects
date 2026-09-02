# Python 解释器切换导致 `yt_dlp` 缺失：跨项目修复交接

**记录日期**：2026-09-02  
**问题项目**：`D:\Dev-Env\Antigravity_Projects\media_scraper`  
**本交接文档所在项目**：`D:\Dev-Env\2026_Work_Tools\Exam_French`  
**原始错误记录**：`D:\Dev-Env\2026_Work_Tools\Exam_French\bugs_01\Conflict_python.exe.txt`

## 1. 工作边界

本文只记录诊断结论和建议执行步骤。当前 `Exam_French` 项目中的 AI 不应修改 `media_scraper` 或其他项目目录；后续应由负责 `media_scraper` 的 AI 在其项目上下文中检查、实施和验证。

不要为了修复此问题而：

- 恢复 Microsoft Store Python 的 `python.exe` 执行别名；
- 将所有项目依赖统一安装到全局 Python；
- 修改 `Exam_French\.venv`；
- 让一个项目复用另一个项目的 `.venv`；
- 未检查工作树就覆盖 `media_scraper` 的用户修改。

## 2. 问题现象

用户在 PowerShell 中运行：

```powershell
cd D:\Dev-Env\Antigravity_Projects\media_scraper
python media_archiver.py "https://www.youtube.com/watch?v=KPK23K7ipVo" --type audio --format mp3 --quality 0
```

下载失败，关键错误为：

```text
C:\Users\John Tan\AppData\Local\Programs\Python\Python313\python.exe: No module named yt_dlp
```

## 3. 已确认的根因

Windows 中的默认 `python` 已从 Microsoft Store Python 3.13.14 切换为 python.org 安装的 Python 3.13.15：

```text
C:\Users\John Tan\AppData\Local\Programs\Python\Python313\python.exe
```

两个 Python 安装拥有相互独立的 `site-packages`：

- 旧 Microsoft Store Python 3.13.14 曾安装 `yt-dlp`；
- 新 Python 3.13.15 没有自动继承旧解释器的第三方包；
- `media_scraper` 当时没有项目专属 `.venv`；
- 因此 `python media_archiver.py` 使用新全局解释器启动，而新解释器找不到 `yt_dlp`。

这不是 Python 3.13.15 不兼容，也不是下载 URL、cookies 或 ffmpeg 导致的当前错误。

## 4. 代码诊断结论

`media_scraper` 的核心代码使用：

```python
[sys.executable, "-m", "yt_dlp", ...]
```

这是正确行为：子进程应使用启动主程序的同一个解释器。当前问题是启动解释器缺少项目依赖，而不是应该把代码改回固定的全局 Python 路径。

该项目 `.gitignore` 已包含：

```gitignore
.venv/
```

因此在项目根目录创建 `.venv` 不应进入 Git。

## 5. 推荐解决方案

为 `media_scraper` 创建自己的 `.venv`，在其中安装 `yt-dlp`，以后始终使用该项目的虚拟环境运行。全局 Python 只作为创建虚拟环境的基础解释器。

预期关系：

```text
全局基础 Python
C:\Users\John Tan\AppData\Local\Programs\Python\Python313\python.exe
    ├── Exam_French\.venv
    └── media_scraper\.venv
```

两个 `.venv` 彼此独立，不能互相替代。

## 6. 给执行 AI 的实施步骤

### 6.1 修改前只读检查

在 PowerShell 中进入目标项目：

```powershell
cd D:\Dev-Env\Antigravity_Projects\media_scraper
```

检查当前解释器和已有环境：

```powershell
python --version
python -c "import sys; print(sys.executable)"
Get-ChildItem -Force | Select-Object Name,Mode,Length,LastWriteTime
```

预期全局解释器为 Python 3.13.15。若 `.venv` 已存在，不要直接覆盖或删除；先读取：

```powershell
Get-Content -Raw -LiteralPath .\.venv\pyvenv.cfg
```

只有确认不存在有效 `.venv` 后，才执行下一步。若需要删除一个已损坏的 `.venv`，必须先获得用户明确授权。

### 6.2 创建项目虚拟环境

优先显式使用已确认的真实基础解释器，避免 WindowsApps 别名回归：

```powershell
& "C:\Users\John Tan\AppData\Local\Programs\Python\Python313\python.exe" -m venv .venv
```

验证：

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable)"
```

预期解释器路径：

```text
D:\Dev-Env\Antigravity_Projects\media_scraper\.venv\Scripts\python.exe
```

### 6.3 安装依赖

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install yt-dlp
```

不要使用含糊的全局命令：

```text
pip install yt-dlp
```

验证安装位置和版本：

```powershell
.\.venv\Scripts\python.exe -m yt_dlp --version
.\.venv\Scripts\python.exe -m pip show yt-dlp
```

`pip show` 的 `Location` 必须位于 `media_scraper\.venv` 中。

### 6.4 使用项目解释器运行

不激活环境的明确运行方式：

```powershell
.\.venv\Scripts\python.exe .\media_archiver.py "https://www.youtube.com/watch?v=KPK23K7ipVo" --type audio --format mp3 --quality 0
```

也可以激活后运行：

```powershell
.\.venv\Scripts\Activate.ps1
python .\media_archiver.py "https://www.youtube.com/watch?v=KPK23K7ipVo" --type audio --format mp3 --quality 0
deactivate
```

PowerShell 命令不要使用 Bash 的 `&&`；顺序执行使用分行或分号，条件执行使用 `if ($?) { ... }`。

## 7. 建议的仓库文件改进

负责 `media_scraper` 的 AI 应先检查现有用户修改，再考虑：

1. 新增或完善 `requirements.txt`，至少声明直接依赖 `yt-dlp`；
2. 更新 `README.md` 和 `README_CN.md`，将安装方式从全局 `pip install yt-dlp` 改为项目 `.venv`；
3. 在 README 中明确 Windows PowerShell 的启动命令；
4. 保持 `.venv/` 在 `.gitignore` 中；
5. 不把本地 `.venv`、下载文件、cookies 或日志提交到 Git。

如果需要可重复构建，执行 AI 应根据该项目的依赖管理策略决定使用：

- 只声明直接依赖的 `requirements.txt`；或
- 固定已经验证的 `yt-dlp` 版本。

不要未经验证就把整个全局 `pip freeze` 写入该项目，因为其中可能混入其他项目的无关包。

## 8. 验收标准

以下条件全部满足才算解决：

1. `media_scraper\.venv\Scripts\python.exe` 可以正常启动；
2. `python -m yt_dlp --version` 在该 `.venv` 中成功；
3. `pip show yt-dlp` 显示安装位置位于该 `.venv`；
4. 原命令不再出现 `No module named yt_dlp`；
5. 不影响 `Exam_French\.venv`；
6. 全局 `python` 仍保持 python.org Python 3.13.15；
7. `.venv` 没有出现在待提交文件中；
8. 若下载仍失败，应作为新的网络、cookies、站点限制或 ffmpeg 问题单独诊断，不能再归因于本次解释器缺包问题。

## 9. 长期环境规则

- 每个 Python 项目单独维护 `.venv`。
- 每个项目记录自己的直接依赖。
- IDE、Codex 和终端都应选择当前项目的 `.venv\Scripts\python.exe`。
- 全局 Python 不承担所有项目的依赖集合。
- 不使用其他项目的虚拟环境来临时运行当前项目。
- 升级或更换全局基础 Python 后，应重建各项目 `.venv`，而不是假定第三方包会自动迁移。

## 10. 本次未执行的操作

本文创建过程中没有：

- 修改 `D:\Dev-Env\Antigravity_Projects\media_scraper`；
- 创建该项目的 `.venv`；
- 安装 `yt-dlp`；
- 修改 README、依赖文件或源代码；
- 执行下载测试；
- 执行任何 Git 操作。
