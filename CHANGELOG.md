# CHANGELOG

## v4.0 - "Production Ready" 🚀 (2026-01-29)

### 🎯 Major Achievements

#### Career Paths Full Coverage (FIXED)
- ✅ Fixed parser regex: `[-−]U(\d+)` - now handles both ASCII hyphen and unicode minus
- ✅ **All 34 Career Paths categories parsed successfully**
- ✅ **16,915 words extracted** from 103 PDFs (up from 4,687)
- ✅ Career Paths now appears in series selection
- ✅ Double-click and Enter key bindings for category selection

#### Advanced Learning Features (NEW)
- ✅ **SM-2 Spaced Repetition Algorithm** (spaced_repetition.py)
  - Adapted to minutes instead of days
  - Quality scoring: 5 → 45 min, 4 → 24 hours, 1 → 5 min
  - Automatic interval adjustment
  
- ✅ **Analytics Manager** (analytics_manager.py)
  - 7-day rolling statistics
  - Session history tracking
  - Accuracy percentage display
  - Most-studied units ranking
  
- ✅ **Difficult Words Deck** (decks_manager.py)
  - Auto-filters words with error_rate > 50%
  - 3x frequency weighting
  - Quick access to problem areas
  
- ✅ **Search & Filter System** (search_filter.py)
  - Search by word phrase
  - Filter by difficulty level
  - Filter by learning status
  - Category-based POS filtering

#### UI/UX Enhancements
- ✅ **Quick Review Mode** (Ctrl+R)
  - Auto-flip after 0.5 seconds
  - Auto-next after 2 seconds
  - Only shows "known" words
  
- ✅ **Enhanced Keyboard Shortcuts**
  - A/D keys for quick no/yes answers
  - Ctrl+R for quick review
  - Ctrl+D for difficult words deck
  - LEFT/RIGHT/SPACE still available
  
- ✅ **Dark Mode Toggle** (settings_manager.py)
  - Persistent settings via .fiszki_config.json
  - Button layout reorganization (2 rows, better spacing)
  
- ✅ **Dashboard Display**
  - 7-day statistics visualization
  - Top units ranking
  - Session completion celebrations

#### Data Completeness
- ✅ **New Enterprise**: 7,612 words (8 files)
- ✅ **English File**: 7,920 words (5 files)
- ✅ **Career Paths**: 16,915 words (103 files, 34 categories) ⭐ NEW FIXED
- ✅ **TOTAL: 32,447 vocabulary entries** ✅ 100% coverage

#### Bug Fixes & Polish
- ✅ Fixed Career Paths category detection in series selection
- ✅ Fixed typos: "podrecznikow" → "podręczników", "serie" → "serię"
- ✅ Added .template folder skip to prevent empty categories
- ✅ Listbox scrollbar for long category lists
- ✅ Categories sorted alphabetically for better UX
- ✅ File counts displayed in category selection
- ✅ Improved error messages and validation

#### Infrastructure
- ✅ Settings persistence (.fiszki_config.json)
- ✅ Analytics persistence (.fiszki_analytics.json)
- ✅ Language support framework (language_manager.py - ready for German)
- ✅ All modules properly documented with docstrings

#### Documentation
- ✅ README.md: Updated features, dataset stats
- ✅ CHANGELOG.md: Comprehensive v4.0 release notes
- ✅ QUICK_REFERENCE.md: Updated keyboard shortcuts and data
- ✅ All files versioned to v4.0

#### Status
- ✅ All features implemented and tested
- ✅ All 32,447 words accessible and searchable
- ✅ Analytics tracking all sessions
- ✅ SM-2 algorithm optimizing learning
- ✅ Ready for public release

---

## v3.7 - "Career Paths Expansion" 📚 (2025-01-29)

### 🎯 Major Achievements

#### Career Paths Support (NEW)
- ✅ Created `career_paths_parser.py` from scratch (272 lines)
- ✅ Supports all 14 Career Paths categories automatically
- ✅ Format: `word [POS-UNIT] definition` with intelligent POS mapping
- ✅ Auto-discovers categories and recursively scans PDF directories
- ✅ Supports unit extraction (U1-U14) from bracket notation
- ✅ Deduplication by (word, unit) key

#### Data Integration  
- ✅ **Career Paths**: 8 categories, 27 PDFs, 4,687 entries
  - Computing: 975 words
  - Electronics: 512 words
  - Food Service Industries: 515 words
  - Industrial Assembly: 550 words
  - Logistics: 550 words
  - Mechanical Engineering: 529 words
  - Science: 515 words
  - Software Engineering: 541 words

#### Grand Total
- ✅ **New Enterprise**: 7,612 entries (8 files)
- ✅ **English File**: 7,920 entries (5 files)
- ✅ **Career Paths**: 4,687 entries (27 files, 8/14 categories)
- ✅ **TOTAL: 20,219 vocabulary entries** (66.7% to 95% coverage goal)

#### Documentation Updates
- ✅ README.md: Added Career Paths format explanation + status table
- ✅ QUICK_REFERENCE.md: Updated data table with Career Paths info
- ✅ All MD files versioned to v3.7

#### Status
- ✅ All three textbook series fully integrated
- ✅ Career Paths auto-detection working perfectly
- ✅ Ready for remaining 6 categories (Accounting, Construction, Engineering, Hotels & Catering, Medical, Mechanics)
- ✅ Gap to 95%: ~7,800 more entries needed

---

## v3.6 - "Growing Project" 🚀 (2025-01-29)

### 🎯 Major Achievements

#### Parser Enhancements
- ✅ English File Parser v3.6: Definition extraction from capitalized sentences
- ✅ Filters Polish words without information (pronunciation/POS)
- ✅ Support for 5 English File levels: Advanced, Intermediate+, Intermediate, Pre-intermediate, Upper-intermediate
- ✅ Total parsed: ~7,920 English File entries

#### GUI Improvements (flashcard_app.py v3.6)
- ✅ Keyboard shortcuts: SPACE (flip), LEFT arrow (no), RIGHT arrow (yes)
- ✅ Real-time session accuracy percentage display
- ✅ Better layout and visual hierarchy
- ✅ Keyboard hints and version info in footer

#### Documentation & Resources
- ✅ README: Added official learning resources + contact for submissions
- ✅ Wayback Machine PDF finding instructions
- ✅ Portfolio link for project visibility
- ✅ All MD files updated to v3.6

#### Data Coverage
- ✅ **New Enterprise**: 8 files, ~7,600+ entries
- ✅ **English File**: 5 files, ~7,920+ entries
- ✅ **Total**: 13 JSON files, ~15,500+ vocabulary entries

---

## v3.0 - 2026-01-29 🎉

### 🔨 Wielka Modernizacja Projektu

#### Parsery - Pełna Przebudowa
- ✅ Usunięto duplikat `new_enterprise-parser.py` (z hyphenem)
- ✅ Przebudowano `new_enterprise_parser.py` - czysty kod, lepsze obsługiwanie błędów
- ✅ Całkowicie przepisano `english_file_parser.py` - konwersja ze skryptu na moduł
- ✅ Obie parsery mają teraz konsystentną strukturę i interfejs
- ✅ Naprawiono ścieżki folderów (bezwzględne zamiast względnych)
- ✅ Dodano obsługę `--full-auto` mode dla obu parserów
- ✅ Obszerne docstringi i komentarze w kodzie
- ✅ Prawidłowa obsługa UTF-8 encoding

#### Aplikacja (flashcard_app.py)
- ✅ Naprawiono dostęp do pola `pronunciation` (było `phonetic`)
- ✅ Dodano obsługę pola `translation` (tłumaczenie)
- ✅ Lepsza prezentacja informacji na karcie flip
- ✅ Wszystkie ścieżki działają niezawodnie z obiema seriami

#### Master Parser
- ✅ Kompletne przepisanie kodu
- ✅ Lepszy interfejs z emotikonami
- ✅ Automatyczne sprawdzanie dostępności serii
- ✅ Diagnostyka problemów dla użytkownika
- ✅ Obsługa wyjątków i error recovery

#### Dokumentacja - KOMPLETNA PRZERÓBKA
- ✅ README.md przepisany od zera (212 linii)
  - Szczegółowa instrukcja obsługi aplikacji
  - Instrukcje parsowania dla obu serii
  - Sekcja rozwiązywania problemów (5 typowych problemów + rozwiązania)
  - Wyjaśnienia jak działają parsery
  - Informacja o systemie powtórek
  - Format JSON ze wszystkimi polami
- ✅ QUICK_REFERENCE.md zaktualizowany (253 linii)
  - Szybki start
  - Tabela troubleshooting
- ✅ FIXES_SUMMARY.md nowy plik (139 linii)
  - Historia zmian
  - Techniczne detale napraw
  - Lista do-to dla przyszłości

#### Kod - Statystyka
- Parsery: 282 + 168 = 450 linii nowego kodu
- Aplikacja: 540 linii (naprawiona)
- Master parser: 187 linii
- Dokumentacja: +200 linii

### 🎯 Status v3.0
- ✅ Wszytkie parsery testowane i działające
- ✅ Aplikacja w pełni funkcjonalna
- ✅ Dokumentacja kompletna
- ✅ Kod czysty i udokumentowany
- ✅ Gotowe do produkcji
- ✅ 100% funkcjonalność

---

## v2.1 - 2025-01-29

### Naprawiono
- Parser English File poprawnie wyodrebnia pojedyncze slowa zamiast calych linii
- Poprawiono regex dla wykrywania slow w English File
- Naprawiono problem pustych JSON po parsowaniu
- Dodano automatyczne tworzenie folderow json/ jesli nie istnieja

### Zmieniono
- Usunieto wszystkie emojis i niestandardowe znaki ze skryptow
- Uproszczono komunikaty w konsolii
- Poprawiono obsluge polskich znakow

## v2.0 - 2025-01-29

### Naprawiono
- Parser English File prawidlowo wyodrebnia slowa (nie cale linie)
- Usunieto nieistniejace serie z GUI (Welttour Deutsch, Career Paths)

### Dodano
- Master parser z menu wyboru serii
- Tryb Full Auto (parsuje wszystkie serie automatycznie)
- Flaga `--full-auto` dla parserow
- Automatyczne wykrywanie dostepnych serii

### Zmieniono
- Parsery obsluguja tryb interaktywny i automatyczny
- Lepsza obsluga bledow w parserach
- Podsumowania po parsowaniu

## v1.0 - 2025-01-27

### Pierwsza wersja
- Aplikacja GUI (Tkinter)
- Parser New Enterprise
- Parser English File (bazowy)
- System wagowy dla slowek
- Zapis postegow do JSON
- Wybor dzialow
- Timer sesji
- Statystyki