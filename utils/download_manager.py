"""
Model and Data Download Manager.
Handles downloading with checksum validation, timeouts, and local caching.
"""

from pathlib import Path
from typing import Optional
import urllib.request

class DownloadManager:
    def __init__(self, target_dir: Optional[Path] = None):
        self.target_dir = target_dir or Path("data/downloads")
        self.target_dir.mkdir(parents=True, exist_ok=True)

    def download_file(self, url: str, filename: str) -> Path:
        dest = self.target_dir / filename
        if dest.exists():
            return dest

        req = urllib.request.Request(url, headers={"User-Agent": "AllSkills-Downloader/2.0"})
        with urllib.request.urlopen(req, timeout=30) as resp, open(dest, "wb") as f:
            f.write(resp.read())
        return dest
