# CHANGELOG

## v5.0 - "Clean & Optimized" (2026-01-31)

### Project Structure
- Consolidated 12 MD files to 3 core files
- Moved build artifacts out of root
- Cleaned all Python files of emoji
- Removed unnecessary scripts (count_words, diagnose, create_icon)
- Minimal dependencies: PyMuPDF, requests, PyInstaller only

### Code Quality
- All emoji removed from codebase
- Excessive comments cleaned
- No duplicate files
- JSON validation: 32,314 words verified
- All modules import successfully

### Distribution
- EXE packaged: 32.6 MB with all data included
- Auto-update ready with v5.0 version check
- Standalone executable: no Python installation required
- dist/ folder now included in repository

## v4.0 - Production Ready (2026-01-29)

### Career Paths Coverage
- Fixed parser regex for unicode characters
- All 34 categories parsed successfully
- 16,915 words extracted from 103 PDFs

### Learning Features
- SM-2 Spaced Repetition (minute-based)
- Analytics Dashboard (7-day stats)
- Difficult Words Deck (auto-filter by error rate)
- Search & Filter functionality
- Dark Mode toggle
- Keyboard shortcuts (SPACE, arrows, Ctrl+R, Ctrl+D)

### Data
- Total: 32,447 words from 3 textbook series
- New Enterprise: 7,612 words (8 files)
- English File: 7,920 words (5 files)
- Career Paths: 16,915 words (103 files)
