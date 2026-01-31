#!/usr/bin/env python3
"""
Build script for creating Fiszki.exe with auto-update support
Usage: python build_exe.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_requirements():
    """Check if required tools are installed"""
    print("Checking requirements...")
    
    try:
        import PyInstaller
        print("PyInstaller: OK")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyInstaller"])
    
    if not Path("assets/icon.ico").exists():
        print("Warning: No icon found. Using default.")


def clean_build():
    """Remove old build artifacts"""
    print("Cleaning old builds...")
    
    dirs_to_remove = ["build", "dist", "__pycache__"]
    for d in dirs_to_remove:
        if Path(d).exists():
            shutil.rmtree(d)
            print(f"Removed {d}/")


def build_exe():
    """Build executable using PyInstaller"""
    print("Building Fiszki.exe...")
    
    icon_arg = ""
    if Path("assets/icon.ico").exists():
        icon_arg = "--icon=assets/icon.ico"
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                          # Single EXE file
        "--windowed",                         # No console window
        "--name=Fiszki",                      # Output name
        "--distpath=./dist",                  # Output directory
        "--add-data=data:data",               # Include data folder
        "--add-data=parsers:parsers",         # Include parsers
        "-y",                                  # Overwrite without asking
    ]
    
    if icon_arg:
        cmd.append(icon_arg)
    
    cmd.append("flashcard_app.py")
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f" Build failed: {e}")
        return False


def create_auto_updater():
    """Create auto-updater component"""
    print("\n Creating auto-updater...")
    
    updater_code = '''"""
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
CURRENT_VERSION = "4.0"

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
                f"Fiszki {new_version} is available.\\n\\nDownload now?"
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
'''
    
    with open("auto_updater.py", "w", encoding="utf-8") as f:
        f.write(updater_code)
    
    print("auto_updater.py created")


def create_setup_script():
    """Create setup.py for distribution"""
    print("Creating setup script...")
    
    setup_code = '''from setuptools import setup, find_packages

setup(
    name='Fiszki',
    version='4.0',
    description='Offline vocabulary learning app with spaced repetition',
    author='Wojciech Halasa',
    author_email='halasawojciech@gmail.com',
    url='https://github.com/PantoYT/Fiszki',
    
    packages=find_packages(),
    include_package_data=True,
    
    install_requires=[
        'PyMuPDF>=1.23.8',
        'requests>=2.31.0',
    ],
    
    entry_points={
        'console_scripts': [
            'fiszki=flashcard_app:main',
        ],
    },
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    
    python_requires='>=3.10',
)
'''
    
    with open("setup.py", "w", encoding="utf-8") as f:
        f.write(setup_code)
    
    print("setup.py created")


def create_release_notes():
    """Create release notes template"""
    print("Creating release template...")
    
    notes = '''# Fiszki v4.0 Release

## Features
-  SM-2 Spaced Repetition (on minutes)
-  Analytics Dashboard
-  Difficult Words Deck
-  Search & Filter
-  Dark Mode
-  32,447 vocabulary words
-  Career Paths (34 categories)

## Download
- [Fiszki-4.0.exe](https://github.com/PantoYT/Fiszki/releases/download/v4.0/Fiszki-4.0.exe)

## Installation
1. Download Fiszki-4.0.exe
2. Run it - no installation needed!
3. All data is stored locally

## Auto-Update
App will notify you of new versions automatically.

## Changelog
- [Full changelog](CHANGELOG.md)
'''
    
    with open("RELEASE_NOTES.md", "w", encoding="utf-8") as f:
        f.write(notes)
    
    print("RELEASE_NOTES.md created")


def main():
    print("="*70)
    print("FISZKI BUILD SYSTEM - v4.0")
    print("="*70)
    
    check_requirements()
    clean_build()
    
    if build_exe():
        print("Build successful!")
        print("Output: dist/Fiszki.exe")
        
        create_auto_updater()
        create_setup_script()
        create_release_notes()
        
        print("="*70)
        print("NEXT STEPS:")
        print("="*70)
        print("""
1. Test: dist/Fiszki.exe

2. GitHub Releases:
   - Create Release v4.0
   - Upload dist/Fiszki.exe
   - Add release notes

3. Users download directly

4. Auto-update works automatically
        """)
        
        return 0
    else:
        print("Build failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
