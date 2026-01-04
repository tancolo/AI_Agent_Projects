# 中文Prompt
这是中文Prompt “用Python抓取网络上，特别是专门提供音乐播放、免费下载的音乐平台，抓取日本歌手滨崎步(Ayumi hamasaki, 浜崎あゆみ)的歌曲，我需要的是*.mp3格式的。

要是无法下载，就给出歌曲的链接，保存到markdown格式文件中。” 我需要对应英文的，方便AI Agent阅读分析

===> 经过Gemini优化后的Prompt
Act as a Python automation expert. I need a script for **educational research purposes** to interact with public music APIs or open web archives.

**Objective:**
Find and archive audio content for the artist **Ayumi Hamasaki (浜崎あゆみ)**.

**Requirements:**
1.  **Source:** Use legal libraries (like `yt-dlp` for YouTube/SoundCloud or other public APIs) to locate the content. Avoid piracy sites.
2.  **Primary Action:** Attempt to download the audio and convert it to **.mp3** format (best quality available).
3.  **Fallback Logic:** If a direct download is restricted or technically failing, **do not fail the script**. Instead, extract the **Song Title** and **Source URL** and append them to a file named `Ayumi_Hamasaki_Links.md`.

**Output:**
Please provide the full Python code with necessary comments explaining how to run it.

