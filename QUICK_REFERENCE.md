# Fiszki - Quick Reference

## Szybki start

```bash
python flashcard_app.py
```

Wybierz podręcznik → Poziom → Działy → Start

## Struktura plików

```
fiszki/
├── flashcard_app.py
├── data/
│   └── {seria}/
│       └── json/
│           └── {poziom}_parsed.json
└── parsers/
    └── master_parser.py
```

## Komendy

### Uruchomienie aplikacji
```bash
python flashcard_app.py
```

### Parsowanie PDF
```bash
python parsers/master_parser.py
```

### Full Auto (wszystkie serie)
```bash
python parsers/master_parser.py
# Opcja 3
```

## Format JSON

```json
[
  {
    "word": "słowo",
    "unit": "1",
    "correct_count": 0,
    "wrong_count": 0
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