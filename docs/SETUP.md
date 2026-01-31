# Installation & Setup

## Requirements

- Python 3.10+
- Tkinter (included with Python)
- 50 MB disk space

## From Source

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run:
```bash
python flashcard_app.py
```

## From EXE (Windows)

Download `Fiszki.exe` from [Releases](https://github.com/PantoYT/Fiszki/releases) and run it.

## Build Your Own EXE

```bash
python scripts/build_exe.py
# Output: dist/Fiszki.exe
```

## Troubleshooting

**PyMuPDF install fails?**
```bash
pip install --upgrade pip setuptools
pip install PyMuPDF
```

**JSON files not loading?**
```bash
python scripts/check_json.py
# Should show: TOTAL: 116 files, 32314 words
```

**Auto-update not working?**
- Check internet connection
- Check GitHub releases: github.com/PantoYT/Fiszki/releases
- Auto-update checks at startup (no manual required)
