# Fiszki v5.0 - Vocabulary Learning Application

**Offline vocabulary learning with 32,447 words | SM-2 Spaced Repetition | No tracking**

## Quick Start

```bash
python flashcard_app.py
```

Choose textbook → Select units → Learn!

## What's Inside

- **32,447 vocabulary words** from 3 textbook series
- **SM-2 Spaced Repetition** algorithm (on minutes, not days)
- **Analytics Dashboard** - 7-day statistics & session history
- **Difficult Words Deck** - Focus on problem areas
- **Search & Filter** - Find words easily
- **Dark Mode** - Eye-friendly interface
- **Keyboard Shortcuts** - SPACE, LEFT/RIGHT, A/D, Ctrl+R, Ctrl+D
- **Auto-update** - Download newest version automatically
- **Offline Mode** - Works without internet
- **100% Private** - Zero tracking, zero data collection

## Data

| Series | Files | Words | Status |
|--------|-------|-------|--------|
| **New Enterprise** | 8 | 7,612 | ✅ |
| **English File** | 5 | 7,920 | ✅ |
| **Career Paths** | 103 | 16,915 | ✅ |
| **TOTAL** | **116** | **32,447** | ✅ |

## Installation

### From Source
```bash
# Install Python 3.10+
pip install -r requirements.txt
python flashcard_app.py
```

### From EXE (Windows)
Download `Fiszki.exe` from [Releases](https://github.com/PantoYT/Fiszki/releases)

## Build EXE

```bash
python scripts/build_exe.py
# Output: dist/Fiszki.exe
```

## Project Structure

```
Fiszki/
├── flashcard_app.py           # Main application
├── requirements.txt           # Dependencies
│
├── app/                       # Application modules
│   ├── analytics_manager.py
│   ├── spaced_repetition.py
│   ├── search_filter.py
│   └── ...
│
├── parsers/                   # PDF parsers
│   ├── new_enterprise_parser.py
│   ├── english_file_parser.py
│   └── career_paths_parser.py
│
├── data/                      # Vocabulary data (32,447 words)
│   ├── new_enterprise/json/
│   ├── english_file/json/
│   └── career_paths/[34 categories]/json/
│
├── scripts/                   # Utility scripts
│   ├── build_exe.py
│   ├── check_json.py
│   └── master_parser.py
│
├── docs/                      # Documentation
│   ├── START_HERE.md
│   ├── SETUP_INSTRUCTIONS.md
│   ├── BUILD_GUIDE.md
│   └── ...
│
└── assets/
    └── fiszki_icon.ico
```

## Documentation

- **[START_HERE.md](docs/START_HERE.md)** - Begin here! Step-by-step guide
- **[SETUP_INSTRUCTIONS.md](docs/SETUP_INSTRUCTIONS.md)** - Installation & configuration
- **[BUILD_GUIDE.md](docs/BUILD_GUIDE.md)** - How to build EXE
- **[DISTRIBUTION.md](docs/DISTRIBUTION.md)** - Distribution & deployment
- **[CHANGELOG.md](docs/CHANGELOG.md)** - Version history
- **[docs/](docs/)** - All documentation

## Features

### Learning
- Flashcard-based vocabulary learning
- Multiple textbooks (New Enterprise, English File, Career Paths)
- Category-based organization
- Unit selection for focused learning

### Intelligence
- SM-2 Spaced Repetition (minute-based intervals)
- Automatic difficulty adjustment
- Session-based analytics
- Error rate tracking

### User Experience
- Dark/Light mode toggle
- Keyboard shortcuts (SPACE, arrows, A/D keys)
- Quick Review Mode (auto-flip, auto-next)
- Progress celebration messages

### Quality of Life
- Auto-save progress
- Offline capability
- No login required
- No data collection
- Auto-update from GitHub

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **SPACE** | Flip card |
| **LEFT / A** | Answer "No" |
| **RIGHT / D** | Answer "Yes" |
| **Ctrl+R** | Quick Review (auto-flip, auto-next) |
| **Ctrl+D** | Difficult Words Deck |
| **ENTER** | Confirm selection in dialogs |

## Requirements

- **Python 3.10+**
- **PyMuPDF 1.23.8** (for PDF parsing)
- **Tkinter** (included with Python)
- **requests** (for auto-update)

## Supported Platforms

- ✅ Windows (EXE or Python)
- ✅ macOS (Python)
- ✅ Linux (Python)

## Future Roadmap

- [ ] Web PWA version (React)
- [ ] Mobile (Kivy/Flutter)
- [ ] Additional languages
- [ ] More textbooks

## License

Open Source - Use freely

## Contact

Email: halasawojciech@gmail.com
GitHub: [PantoYT/Fiszki](https://github.com/PantoYT/Fiszki)

---

**Ready to learn? Download and start! 🚀**
