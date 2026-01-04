import configparser
from pathlib import Path
from typing import Dict, List, Any

class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = configparser.ConfigParser()
        # Preserve case sensitive options if needed, but usually INI keys are lower
        
    def load(self) -> Dict[str, Any]:
        """Load and parse the configuration file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
            
        self.config.read(self.config_path, encoding='utf-8')
        
        parsed_config = {
            "general": {},
            "artists": []
        }
        
        # Load General Settings
        if "General" in self.config:
            gen = self.config["General"]
            parsed_config["general"] = {
                "media_type": gen.get("media_type", "audio"),
                "format": gen.get("format", "webm"),
                "quality": gen.get("quality", "best"),
                "max_results": gen.getint("max_results", 5),
                "ffmpeg_location": gen.get("ffmpeg_location", "")
            }
            
        # Load Artists
        for section in self.config.sections():
            if section.startswith("Artist:"):
                artist_name = section.split(":", 1)[1]
                defaults = parsed_config["general"]
                sec = self.config[section]
                
                # Determine search keywords
                if "keywords" in sec:
                    keywords = [k.strip() for k in sec["keywords"].split(",")]
                else:
                    keywords = [f"{artist_name} official"]
                    
                parsed_config["artists"].append({
                    "name": artist_name,
                    "output_folder": sec.get("output_folder", artist_name),
                    "keywords": keywords,
                    "media_type": sec.get("media_type", defaults["media_type"]),
                    "format": sec.get("format", defaults["format"]),
                    "quality": sec.get("quality", defaults["quality"])
                })
                
        return parsed_config
