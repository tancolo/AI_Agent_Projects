"""
Debug Script: Compare V0.1 and V0.2 Download Results
=====================================================
This script compares the files downloaded by:
  - V0.1 (ayumi_hamasaki_archiver.py) -> downloads/ayumi_hamasaki/
  - V0.2 (media_archiver.py)          -> downloads/Ayumi Hamasaki/

It will report:
  - File counts
  - Files only in V0.1
  - Files only in V0.2
  - Common files
"""

from pathlib import Path
import os

def get_mp3_files(folder: Path) -> set:
    """Get set of MP3 filenames (normalized) from a folder."""
    if not folder.exists():
        return set()
    # Normalize: lowercase, remove extra spaces
    return {f.name.lower().replace("  ", " ").strip() for f in folder.glob("*.mp3")}

def main():
    v01_folder = Path("downloads/ayumi_hamasaki")
    v02_folder = Path("downloads/Ayumi Hamasaki")
    
    print("=" * 60)
    print("MEDIA SCRAPER - V0.1 vs V0.2 COMPARISON")
    print("=" * 60)
    
    # Get all files
    v01_all = set(os.listdir(v01_folder)) if v01_folder.exists() else set()
    v02_all = set(os.listdir(v02_folder)) if v02_folder.exists() else set()
    
    print(f"\n📁 V0.1 Folder ({v01_folder}): {len(v01_all)} total files")
    print(f"📁 V0.2 Folder ({v02_folder}): {len(v02_all)} total files")
    
    # Filter MP3 only
    v01_mp3 = get_mp3_files(v01_folder)
    v02_mp3 = get_mp3_files(v02_folder)
    
    print(f"\n🎵 V0.1 MP3 Count: {len(v01_mp3)}")
    print(f"🎵 V0.2 MP3 Count: {len(v02_mp3)}")
    
    # Differences
    only_in_v01 = v01_mp3 - v02_mp3
    only_in_v02 = v02_mp3 - v01_mp3
    common = v01_mp3 & v02_mp3
    
    print(f"\n✅ Common MP3s: {len(common)}")
    print(f"⚠️  Only in V0.1: {len(only_in_v01)}")
    print(f"⚠️  Only in V0.2: {len(only_in_v02)}")
    
    if only_in_v01:
        print("\n--- Files ONLY in V0.1 (missing from V0.2): ---")
        for f in sorted(only_in_v01):
            print(f"  - {f}")
    
    if only_in_v02:
        print("\n--- Files ONLY in V0.2 (new in V0.2): ---")
        for f in sorted(only_in_v02):
            print(f"  - {f}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
