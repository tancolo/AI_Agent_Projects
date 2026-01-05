# Prompt EN V0.1
Act as a Python automation expert. I need a script for **educational research purposes** to interact with public music APIs or open web archives.

**Objective:**
Find and archive audio content for the artist **Ayumi Hamasaki (浜崎あゆみ)**.

**Requirements:**
1.  **Source:** Use legal libraries (like `yt-dlp` for YouTube/SoundCloud or other public APIs) to locate the content. Avoid piracy sites.
2.  **Primary Action:** Attempt to download the audio and convert it to **.mp3** format (best quality available).
3.  **Fallback Logic:** If a direct download is restricted or technically failing, **do not fail the script**. Instead, extract the **Song Title** and **Source URL** and append them to a file named `Ayumi_Hamasaki_Links.md`.

**Output:**
Please provide the full Python code with necessary comments explaining how to run it.

# Prompt EN V0.2
Refactor the script into a universal, configuration-based media scraping tool with the following requirements:
1. Replace all mentions of "Ayumi Hamasaki" and her Japanese name with variables for easier modification. Python filenames should not contain specific artist names (like `ayumi_hamasaki`); use generic names instead.
2. The `download` directory should contain subfolders for different artists, with folder names matching the artist names. For example, if the config includes Bruno Mars, Ayumi Hamasaki, and Taylor Swift, there should be three corresponding folders under `download`, each containing that artist's tracks.
3. **Config-based Driving**: Use a Git-like configuration format (e.g., INI format) to dynamically read scraping tasks.
4. **Dynamic Search Targets**: Support setting artist names or specific search keywords in the configuration file. The Python program should iterate through each artist in the config and perform searches accordingly.
5. **Media Type Switching**: Support choosing between `Audio` or `Video` for the scrape.
6. **Multi-format Packaging**: Support various formats such as `mp3`, `webm`, and `mp4`. The default packaging format should be `webm`.
7. **Download Quality Control**:
   - **Audio**: Allow setting the bitrate (e.g., 320kbps); defaults to the highest available bitrate.
   - **Video**: Allow setting the resolution (e.g., 1080p); defaults to `720p`.
8. **Fallback Mechanism**: If the script cannot complete a download directly, extract the original link and save it to a Markdown file. There should be a `markdown` folder in the project to store link info for failed downloads for each artist, similar to the current `Ayumi_Hamasaki_Links.md`. For example, if Bruno Mars, Ayumi Hamasaki, and Taylor Swift all have failed links, there should be three corresponding files in the `markdown` folder.
9. Do not rush to execute the script. First, fully understand the upgrade requirements, then output your upgrade strategy and a subsequent execution plan.
# Prompt EN V0.3
Current V0.2 script is working well, but needs to be upgraded to support ad-hoc direct downloading from URLs (e.g., YouTube Shorts) in addition to the config-based batch mode.
1.  **Dual Mode Requirement**: The script should support both the existing configuration-driven mode and a new "Direct URL" mode.
    -   **Config Mode**: Continues to work as before (reading artists from config).
    -   **Direct URL Mode**: Allows running the script with a specific YouTube URL (or other supported URL) argument to download it directly without editing the config file.
2.  **Extensibility**: Design the solution to be modular and extensible for future needs, rather than just a quick hack. It should ideally be integrated into the main script structure.
3.  **Artifact Management**: The generated planning artifacts (`implementation_plan.md`, `walkthrough.md`, `task.md`) should not overwrite the previous V0.2 versions. Instead, use a version suffix logic (e.g., `implementation_plan_V0.3.md`) to preserve the history of the project evolution.
4.  **Process**: Do not rush to code. First, analyze the requirements and provide a detailed upgrade strategy and execution plan (saved as V0.3 artifacts) for review.
