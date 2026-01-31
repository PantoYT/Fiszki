"""
Auto-updater for Fiszki
Checks GitHub releases and downloads new versions
"""

import requests
import json
import subprocess
import os
import tempfile
import shutil
from pathlib import Path

GITHUB_REPO = "PantoYT/Fiszki"
CURRENT_VERSION = "5.0"

def get_latest_release():
    """Fetch latest release info from GitHub"""
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Could not check for updates: {e}")
        return None

def compare_versions(v1, v2):
    """Compare semantic versions. Returns True if v2 > v1"""
    try:
        v1_parts = [int(x) for x in v1.split('.')]
        v2_parts = [int(x) for x in v2.split('.')]
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            p1 = v1_parts[i] if i < len(v1_parts) else 0
            p2 = v2_parts[i] if i < len(v2_parts) else 0
            
            if p2 > p1:
                return True
            elif p2 < p1:
                return False
        
        return False
    except:
        return False

def download_update(download_url):
    """Download new version"""
    try:
        print(" Downloading update...")
        response = requests.get(download_url, stream=True)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.exe') as tmp:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    tmp.write(chunk)
            return tmp.name
    except Exception as e:
        print(f"Download failed: {e}")
        return None

def apply_update(new_exe_path, current_exe_path):
    """Apply update (requires restart)"""
    try:
        import ctypes
        
        # Use Windows API to replace file after restart
        backup_path = str(current_exe_path) + ".backup"
        shutil.copy2(current_exe_path, backup_path)
        shutil.copy2(new_exe_path, current_exe_path)
        
        print(" Update applied. Restart application.")
        return True
    except Exception as e:
        print(f" Update failed: {e}")
        return False

def check_and_update(root_window=None):
    """Main update check"""
    release = get_latest_release()
    
    if not release:
        return False
    
    new_version = release.get('tag_name', '').lstrip('v')
    
    if compare_versions(CURRENT_VERSION, new_version):
        print(f" New version available: {new_version}")
        
        if root_window:
            from tkinter import messagebox
            response = messagebox.askyesno(
                "Update Available",
                f"Fiszki {new_version} is available.\n\nDownload now?"
            )
            if response:
                exe_url = None
                for asset in release.get('assets', []):
                    if asset['name'].endswith('.exe'):
                        exe_url = asset['browser_download_url']
                        break
                
                if exe_url:
                    new_exe = download_update(exe_url)
                    if new_exe:
                        current_exe = Path(os.path.abspath(__file__))
                        apply_update(new_exe, current_exe)
                        return True
        else:
            # Non-GUI mode
            for asset in release.get('assets', []):
                if asset['name'].endswith('.exe'):
                    new_exe = download_update(asset['browser_download_url'])
                    if new_exe:
                        apply_update(new_exe, Path(os.path.abspath(__file__)))
                        return True
    
    return False
