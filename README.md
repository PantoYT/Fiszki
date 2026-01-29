# Fiszki v4.0

Offline'owa aplikacja desktopowa do nauki słownictwa z PDF-ów.  
**Bez kont. Bez logowania. Bez śledzenia.**

## 🚀 Szybki start

```bash
# Uruchom aplikację
python flashcard_app.py

# Parsuj PDF-y
python parsers/master_parser.py
```

## 📊 Status

| Seria | Pliki | Słówek | Status |
|-------|-------|--------|--------|
| **New Enterprise** | 8 | 7,612 | ✅ |
| **English File** | 5 | 7,920 | ✅ |
| **Career Paths** | 103 | 16,915 | ✅ |
| **RAZEM** | **116** | **32,447** | ✅ |

**Parser dokładność: ~98%**  
**Status: Production-ready** 🎯

## ✨ Features v4.0

### Core Features
- 📚 Nauka słownictwa w formie fiszek
- 🔌 W pełni offline
- 🔒 Prywatne dane
- 💾 Auto-save postępu

### Intelligent Learning (NEW v4.0)
- 🧠 **SM-2 Spaced Repetition** - Algorytm naukowy na minuty (nie dni!)
- 📊 **Analytics Dashboard** - 7-dniowe statystyki, roczna historia
- 🎯 **Difficult Words Deck** - Automatyczne filtrowanie słów (error_rate > 50%)
- 🔍 **Search & Filter** - Szukaj po słowach, filtruj po poziomie trudności
- 🏆 **Quick Review Mode** - Ctrl+R: auto-flip 0.5s, auto-next 2s

### UI/UX Improvements
- ⌨️ Skróty klawiszowe: SPACE, LEFT/RIGHT/A/D, Ctrl+R, Ctrl+D
- 🌙 Dark mode toggle
- 🎨 Responsywny interfejs
- 📱 Kategoryzacja słów po częściach mowy

## 📖 Dokumentacja

- [Pełna dokumentacja](README_FULL.md) - Instrukcje szczegółowe
- [Quick Reference](QUICK_REFERENCE.md) - Szybkie instrukcje
- [Changelog](CHANGELOG.md) - Historia zmian

## 🔧 Wymagania

- Python 3.10+
- Tkinter (domyślnie)
- PyMuPDF 1.23.8 - `pip install PyMuPDF`

## 📁 Struktura

```
fiszki/
├── flashcard_app.py              # Główna aplikacja
├── master_parser.py              # Manager parserów
├── spaced_repetition.py          # SM-2 algorytm
├── analytics_manager.py          # Statystyki nauki
├── search_filter.py              # Wyszukiwanie i filtrowanie
├── decks_manager.py              # Difficult words deck
├── settings_manager.py           # Ustawienia i dark mode
│
├── parsers/
│   ├── master_parser.py
│   ├── new_enterprise_parser.py
│   ├── english_file_parser.py
│   └── career_paths_parser.py
│
├── data/                         # Baza danych
│   ├── new_enterprise/json/      # 7,612 słów
│   ├── english_file/json/        # 7,920 słów
│   └── career_paths/[34 cat]/json/ # 16,915 słów (34 kategorie)
│
├── README.md                     # Główna dokumentacja
├── CHANGELOG.md                  # Historia zmian
├── QUICK_REFERENCE.md            # Szybka referenca
└── requirements.txt              # Zależności
```

## 🎯 SM-2 Spaced Repetition (v4.0)

Opiera się na algorytmie "Supermemo 2", ale **na minuty zamiast dni**:
- Jakość 5: powtórzenie za ~45 minut
- Jakość 4: powtórzenie za ~24 godziny
- Jakość 1: powtórzenie za ~5 minut

Automatycznie dostosowuje interwały na podstawie historii odpowiedzi.

## 📞 Kontakt

Brakuje Ci książki? Wyślij propozycję na: `halasawojciech@gmail.com`

## 📝 Licencja

Projekt otwarty. Użyj swobodnie.

---

**Wersja:** 4.0 | **Status:** Production-ready ✅  
**Dataset:** 32,447 słów (3 serie, 116 plików)  
**Ostatnia aktualizacja:** 29.01.2026
