# Fiszki v4.0 - Quick Reference

Szybkie instrukcje dla zainteresowanych.

## 🚀 Szybki start

```bash
# Uruchom aplikację
python flashcard_app.py

# Kliknij: Zaladuj podręcznik → Seria → Kategoria → Zaznacz działy → Start
```

## ⌨️ Keyboard Shortcuts

| Klawisz | Akcja |
|---------|-------|
| SPACE | Przewróć kartę |
| LEFT arrow / A | Nie znam (błąd) |
| RIGHT arrow / D | Znam (OK) |
| Ctrl+R | Quick Review (auto-flip 0.5s, auto-next 2s) |
| Ctrl+D | Difficult Words Deck |
| ENTER | Potwierdź wybór w dialogach |

## 📖 Parsowanie PDF-ów

### Master Parser (najwygodniej)
```bash
python master_parser.py
```
Wybierz serię i opcję (1, 2, lub 3 - FULL AUTO)

### Bezpośrednio
```bash
# New Enterprise - automatycznie
python parsers/new_enterprise_parser.py --full-auto

# English File - automatycznie (5 plików)
python parsers/english_file_parser.py --full-auto

# Career Paths - automatycznie (wszystkie kategorie)
python parsers/career_paths_parser.py --full-auto
```

## 📊 Aktualne dane (v4.0)

| Seria | Kategorie | Pliki | Słówek | Status |
|-------|-----------|-------|--------|--------|
| **New Enterprise** | - | 8 | 7,612 | ✅ OK |
| **English File** | 5 poziomów | 5 | 7,920 | ✅ OK |
| **Career Paths** | 34 kategorie | 103 | 16,915 | ✅ OK (FIXED!) |

**RAZEM: 32,447 słów** ✅ (100% pokrycie)

## 📁 Katalogi

```
fiszki/
├── flashcard_app.py              ← Aplikacja (v4.0)
├── master_parser.py              ← Zarządca parserów
├── spaced_repetition.py          ← SM-2 algorytm (NEW)
├── analytics_manager.py          ← Statystyki (NEW)
├── search_filter.py              ← Wyszukiwanie (NEW)
├── decks_manager.py              ← Difficult deck (NEW)
├── settings_manager.py           ← Dark mode (NEW)
│
├── data/
│   ├── new_enterprise/json/      ← 7,612 słów
│   ├── english_file/json/        ← 7,920 słów
│   └── career_paths/[34 cat]/    ← 16,915 słów (FIXED)
│       ├── Accounting/json/
│       ├── Agriculture/json/
│       ├── Computing/json/
│       └── ... [34 total]
│
└── parsers/
    ├── master_parser.py
    ├── new_enterprise_parser.py
    ├── english_file_parser.py
    └── career_paths_parser.py
```

## 🧠 SM-2 Spaced Repetition (v4.0 NEW)

```
Jakość → Interwał
─────────────────
5      → ~45 min
4      → ~24 hours
3      → ~3 dni
2      → ~1 dzień
1      → ~5 min
```

## 📊 Analytics Dashboard (v4.0 NEW)

Kliknij "Statystyki":
- 📈 7-dniowe wykresy
- 🏆 Top jednostki
- 📝 Historia sesji
- ✅ Procent dokładności

## 🎯 Difficult Words Deck (v4.0 NEW)

Kliknij "Trudne" → ćwicz tylko słowa z error_rate > 50%

## 🔍 Search & Filter (v4.0 NEW)

Kliknij "Szukaj" → wyszukaj/filtruj słowa

## 📋 Format JSON

```json
[
  {
    "word": "hello",
    "pronunciation": "həˈləʊ",
    "part_of_speech": "noun",
    "definition": "greeting",
    "translation": "cześć",
    "unit": "U1",
    "error_rate": 0.0,
    "last_review": "2026-01-29T10:30:00",
    "sr_interval": 45,
    "sr_repetitions": 3,
    "sr_ease": 2.5
  }
]
```

## 🎯 Instrukcja aplikacji

1. Kliknij **"Zaladuj podręcznik"**
2. Wybierz serię (New Enterprise / English File / Career Paths)
3. Wybierz kategorię/plik
4. **Zaznacz** działy które chcesz powtarzać
5. Kliknij **"Start"** i ucz się!

**Podczas sesji:**
- Czytasz słówko, myślisz nad odpowiedzią
- Wciskasz SPACE aby zobaczyć odpowiedź
- LEFT/A = nie znam (błąd), RIGHT/D = znam (OK)
- Aplikacja śledzi Twój postęp

## 💡 Pro Tips

- **Szybka sesja:** Ctrl+R (auto-flip 0.5s, auto-next 2s)
- **Trudne słowa:** Ctrl+D (słowa z error_rate > 50%)
- **Szukanie:** Kliknij Szukaj → wpisz słowo/definicję
- **Dark mode:** Toggle w ustawieniach
- **Offline:** Wszystko działa bez internetu

---

**Wersja:** 4.0 | **Ostatnia aktualizacja:** 29.01.2026  
**Dataset:** 32,447 słów | **Status:** Production-ready ✅
- Kliknij **"Przewróć"** aby zobaczyć wymowę, definicję, tłumaczenie
- Oceń siebie: **"Znam"** lub **"Nie znam"**
- Postęp jest automatycznie zapisywany

## ⚙️ Waga powtórek

```
waga = max(1, 10 + (błędy × 2) - poprawne)
```

Trudne słówka pojawiają się częściej!

## 🐛 Problemy

| Problem | Rozwiązanie |
|---------|------------|
| "Brak serii" | Dodaj PDF-y i sparsuj: `python master_parser.py` |
| "No module 'fitz'" | `pip install PyMuPDF` |
| Parser nie widzi PDF | Sprawdź: `data/<seria>/pdf/` zawiera `*.pdf` |
| Znaki źle się wyświetlają | JSON jest UTF-8 (domyślnie) |
| Aplikacja się nie uruchamia | Sprawdź Tkinter: `python -m tkinter` |

## 📚 Wymagania

- Python 3.10+
- Tkinter (domyślnie)
- PyMuPDF (opcjonalnie)
  }
]
```

## Obsługa aplikacji

### Wybór fiszek
1. "Wybierz podręcznik" → Seria
2. Wybierz poziom
3. Zaznacz działy
4. Start

### Podczas nauki
- **Przewróć**: pokazuje odpowiedź
- **Znam**: +1 do correct_count
- **Nie znam**: +1 do wrong_count
- **Stop**: kończy sesję

### System wagowy

Częstotliwość = `10 + (wrong_count * 2) - correct_count`

Więcej błędów = częstsze pojawianie się

## Parsery

### Obsługiwane serie
- New Enterprise (`\pronunciation\` format)
- English File (`/phonetic/` format)

### Tryby parsowania
- **Automatyczny**: parsuje wszystko bez pytania
- **Ręczny**: potwierdza każdy wpis (t/n/q)
- **Full Auto**: parsuje wszystkie pliki ze wszystkich serii

### Wymagania
```bash
pip install PyMuPDF
```

### Lokalizacja PDF
```
data/{seria}/pdf/*.pdf
```

### Output
```
data/{seria}/json/{nazwa}_parsed.json
```

## Rozwiązywanie problemów

### Brak serii w GUI
```
Sprawdź: data/*/json/*_parsed.json istnieją
```

### Parser nie działa
```bash
pip install PyMuPDF
# Sprawdź czy PDF jest tekstem, nie skanem
```

### Brak zapisu postępów
```
Sprawdź uprawnienia zapisu: data/*/json/
```

### Błąd parsowania
```
Użyj trybu ręcznego (opcja 2)
Sprawdź format PDF
```

## Dodawanie nowej serii

### Bez parsera (masz gotowe JSON)
1. Utwórz `data/nazwa/json/`
2. Dodaj `poziom_parsed.json`
3. Gotowe

### Z parserem (masz PDF)
1. Utwórz `data/nazwa/pdf/`
2. Dodaj pliki PDF
3. Napisz `parsers/nazwa_parser.py`
4. Dodaj do `master_parser.py`

## Wskazówki

### Efektywna nauka
- Zaznacz 2-3 działy naraz
- Ucz się regularnie (codziennie)
- Nie pomijaj błędnych słówek

### Zarządzanie plikami
- Backup: kopiuj `data/*/json/`
- Reset: usuń `*_parsed.json` i parsuj ponownie
- Merge: połącz JSON ręcznie (lista obiektów)

### Parsowanie
- Zawsze sprawdź wynik w trybie ręcznym pierwszy raz
- Full Auto używaj gdy znasz format PDF
- Loguj błędy dla nowych serii

## Skróty klawiszowe

Brak (obsługa myszką)

## Statystyki

Wyświetlane po Stop:
- Słówek w działach
- Poprawne (suma)
- Błędne (suma)

## Limit czasowy

Brak (nauka do momentu kliknięcia Stop)

## Pliki konfiguracyjne

Brak (seria i poziom wybierane przez GUI)

## Eksport danych

JSON można otworzyć w:
- Edytorze tekstu
- Excel (Import JSON)
- Python (json.load)

## Backup

Kluczowe pliki:
```
data/*/json/*_parsed.json  (postępy + słówka)
```

## Reset postępów

### Pojedyncze słowo
Edytuj JSON:
```json
"correct_count": 0,
"wrong_count": 0
```

### Cały plik
Parsuj PDF ponownie lub edytuj masowo

## Parser - szczegóły techniczne

### New Enterprise
```
Format: word \pronunciation\ (pos) = definition
Regex: \\([^\\]+)\\
```

### English File
```
Format: word pos /phonetic/ definition translation
Regex: /([^/]+)/
```

### Detekcja jednostek
```
New Enterprise: Unit \d+[a-z]
English File: File \d+ | Unit \d+
```

## Logi

Parsery wyświetlają:
- Jednostki wykryte
- Słówka sparsowane
- Błędy (jeśli są)

Aplikacja:
- Brak logów (GUI)

## Instalacja zależności

```bash
# Aplikacja
# Brak (Tkinter wbudowany)

# Parsery
pip install PyMuPDF
```

## Compatybilność

- Python 3.10+
- Windows / Linux / macOS
- Tkinter wymagany

## Wsparcie

1. Sprawdź Troubleshooting w README
2. Sprawdź format JSON
3. Użyj trybu ręcznego parsera

## Szybkie komendy

```bash
# Start
python flashcard_app.py

# Parse wszystko
python parsers/master_parser.py
# → 3 (Full Auto)

# Parse jedną serię
python parsers/new_enterprise_parser.py
# → 1 (Auto) lub 2 (Ręczny)

# Sprawdź JSON
cat data/new_enterprise/json/b1_parsed.json | head

# Backup
cp -r data/*/json/ backup/
```

---

Wydrukuj lub zapisz jako bookmark.