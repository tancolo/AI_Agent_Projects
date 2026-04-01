import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from .utils import log_message, ensure_directory

class MediaScraper:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.general_config = config.get("general", {})
        self.output_base = Path("./downloads")
        self.links_base = Path("./markdown_links")
        self.log_file = Path("archiver_log.txt")
        self.ffmpeg_location = self.general_config.get("ffmpeg_location", "")
        self.max_results = self.general_config.get("max_results", 5)

    def _get_ffmpeg_args(self) -> List[str]:
        """Return ffmpeg-location arguments if configured."""
        if self.ffmpeg_location:
            return ["--ffmpeg-location", self.ffmpeg_location]
        return []

    def initialize_links_file(self, artist_name: str) -> Path:
        """Initialize or update the artist's links markdown file."""
        ensure_directory(self.links_base)
        # Use artist name for file: Bruno_Mars_Links.md
        safe_name = "".join(c for c in artist_name if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
        links_file = self.links_base / f"{safe_name}_Links.md"
        
        header = f"""# {artist_name} - Audio/Video Archive Links

> **Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
> **Purpose:** Educational research - archiving publicly available content

---

## Download Failures / Restricted Content

"""
        if not links_file.exists():
            with open(links_file, "w", encoding="utf-8") as f:
                f.write(header)
            log_message(f"Created links file: {links_file}", "INFO", self.log_file)
            
        return links_file

    def append_to_links_file(self, links_file: Path, title: str, url: str, reason: str) -> None:
        """Append a failed download entry to the markdown file."""
        entry = f"""### {title}
- **URL:** [{url}]({url})
- **Reason:** {reason}
- **Added:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

"""
        with open(links_file, "a", encoding="utf-8") as f:
            f.write(entry)
        log_message(f"Added to links file: {title}", "INFO", self.log_file)

    def search_youtube(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search YouTube for videos."""
        log_message(f"Searching for: {query}", "INFO", self.log_file)
        
        try:
            cmd = [
                sys.executable, "-m", "yt_dlp",
                "--dump-json",
                "--flat-playlist",
                "--no-warnings",
                f"ytsearch{max_results}:{query}"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                encoding="utf-8",
                errors="replace"
            )
            
            videos = []
            if result.stdout:
                for line in result.stdout.strip().split("\n"):
                    if line:
                        try:
                            video_info = json.loads(line)
                            videos.append({
                                "id": video_info.get("id", ""),
                                "title": video_info.get("title", "Unknown Title"),
                                "url": video_info.get("url") or f"https://www.youtube.com/watch?v={video_info.get('id', '')}",
                            })
                        except json.JSONDecodeError:
                            continue
            
            log_message(f"Found {len(videos)} videos for query: {query}", "INFO", self.log_file)
            return videos
            
        except Exception as e:
            log_message(f"Search error: {e}", "ERROR", self.log_file)
            return []

    def download_media(self, video_url: str, title: str, artist_output_path: Path, artist_config: Dict[str, Any]) -> bool:
        """Download media based on artist configuration."""
        
        media_type = artist_config["media_type"]
        fmt = artist_config["format"]
        quality = artist_config["quality"]
        
        # Handle output template based on whether we have a specific title
        if title is None:
            # Auto-title mode: let yt-dlp use the video's actual title
            output_template = str(artist_output_path / "%(title)s.%(ext)s")
            log_message(f"Attempting download (auto-title): {video_url}", "INFO", self.log_file)
        else:
            # Manual title mode: sanitize and use provided title
            log_message(f"Attempting download: {title}", "INFO", self.log_file)
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_', '.')).strip()
            safe_title = safe_title[:100]
            output_template = str(artist_output_path / f"{safe_title}.%(ext)s")
        
        cmd = [sys.executable, "-m", "yt_dlp"]
        
        # Configure arguments based on media type
        if media_type == "audio":
            cmd.extend([
                "--extract-audio",
                "--audio-format", fmt,
            ])
            # If quality is a number (0-9), use --audio-quality, else use --bitrate logic if supported or assume yt-dlp handles "320K" as quality often
            # yt-dlp --audio-quality accepts 0-9 or specific bitrate (e.g. 192K)
            cmd.extend(["--audio-quality", str(quality)])
            
        else: # video
            # Video logic
            # Quality defaults to 720p if not specified properly, but here we expect strings like '1080p'
            res_val = quality.replace('p', '')
            if res_val.isdigit():
                # Download best video <= resolution + best audio, merge
                cmd.extend([
                    "-f", f"bestvideo[height<={res_val}]+bestaudio/best[height<={res_val}]",
                    "--merge-output-format", fmt
                ])
            else:
                # Fallback if quality format is weird or "best"
                 cmd.extend(["-f", "bestvideo+bestaudio/best"])

        # Common arguments
        cmd.extend([
            "--embed-thumbnail",
            "--add-metadata",
            "--no-playlist",
            "--output", output_template,
            "--no-warnings",
            "--progress"
        ])
        
        # Automatically use cookies if the file exists
        if Path("cookies.txt").exists():
            cmd.extend(["--cookies", "cookies.txt"])
        
        cmd.extend(self._get_ffmpeg_args())
        cmd.append(video_url)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600, # 10 minutes
                encoding="utf-8",
                errors="replace"
            )
            
            if result.returncode == 0:
                success_msg = f"Successfully downloaded: {title if title else video_url}"
                log_message(success_msg, "SUCCESS", self.log_file)
                return True
            else:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                log_msg = f"Download failed for {title if title else video_url}: {error_msg}"
                log_message(log_msg, "WARNING", self.log_file)
                return False
                
        except Exception as e:
            log_message(f"Download exception: {e}", "ERROR", self.log_file)
            return False

    def run(self):
        """Main execution loop."""
        artists = self.config.get("artists", [])
        if not artists:
            log_message("No artists configured.", "WARNING", self.log_file)
            return

        for artist in artists:
            name = artist["name"]
            log_message(f"Processing artist: {name}", "INFO", self.log_file)
            
            # Setup directories
            output_path = self.output_base / artist["output_folder"]
            ensure_directory(output_path)
            
            links_file = self.initialize_links_file(name)
            
            processed_urls = set()
            
            for query in artist["keywords"]:
                videos = self.search_youtube(query, self.max_results)
                
                for video in videos:
                    url = video["url"]
                    if url in processed_urls:
                        continue
                    processed_urls.add(url)
                    
                    success = self.download_media(url, video["title"], output_path, artist)
                    
                    if not success:
                        self.append_to_links_file(links_file, video["title"], url, "Download restricted or failed")

    def download_direct(self, url: str) -> bool:
        """
        Download a single URL directly using general config settings.
        Used for ad-hoc downloads via CLI.
        """
        log_message(f"Direct download requested: {url}", "INFO", self.log_file)
        
        # Setup output directory
        output_path = self.output_base / "Direct_Downloads"
        ensure_directory(output_path)
        
        # Initialize links file for direct downloads
        links_file = self.initialize_links_file("Direct_Downloads")
        
        # Create a temporary "artist config" using general settings
        temp_config = {
            "media_type": self.general_config.get("media_type", "audio"),
            "format": self.general_config.get("format", "webm"),
            "quality": self.general_config.get("quality", "best")
        }
        
        # Pass None as title to enable auto-titling from yt-dlp metadata
        # Attempt download
        success = self.download_media(url, None, output_path, temp_config)
        
        if not success:
            # For failed downloads, use URL as fallback identifier
            fallback_title = url.split("/")[-1] or "direct_download"
            self.append_to_links_file(links_file, fallback_title, url, "Direct download failed")
            
        return success
