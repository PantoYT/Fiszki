# Fiszki - Aplikacja do nauki słownictwa

Prosta, offline'owa aplikacja desktopowa do nauki słownictwa z plików JSON.  
**Bez kont. Bez logowania. Bez śledzenia. Bez rozpraszaczy.**

## ✨ Cechy

- 📚 Nauka słownictwa w formie fiszek
- 🔌 W pełni offline - działa bez internetu
- 🔒 Żadne dane nie opuszczają twojego komputera
- 📊 System powtórek oparty na liczbie błędów
- 📖 Obsługa wielu serii podręczników (New Enterprise, English File, itp.)
- 🎯 Wybór konkretnych działów/sekcji do nauki
- ⏱️ Licznik czasu sesji
- 💾 Automatyczne zapisywanie postępu

## 📋 Wymagania

- **Python 3.10+**
- **Tkinter** (zazwyczaj domyślnie w instalacji Pythona)
- **PyMuPDF** (`fitz`) - tylko jeśli będziesz parsować PDF-y

## 🚀 Szybki start

### 1. Instalacja

```bash
# Sklonuj repozytorium
git clone <repo-url>
cd fiszki

# Zainstaluj zależności (opcjonalne - tylko dla parserów)
pip install PyMuPDF
```

### 2. Uruchomienie aplikacji

```bash
python flashcard_app.py
```

## 📖 Instrukcja obsługi

### Aplikacja (flashcard_app.py)

1. **Wybierz podręcznik** - Kliknij "Wybierz podręcznik" aby wybrać serię (np. New Enterprise)
2. **Wybierz poziom** - Zaznacz plik z konkretnym poziomem (A1, A2, B1, etc.)
3. **Wybierz działy** - Zaznacz które działy chcesz powtarzać
4. **Rozpocznij naukę** - Kliknij "Start" aby rozpocząć sesję

**Podczas nauki:**
- Przeczytaj słówko na karcie
- Kliknij "Przewróć" aby zobaczyć wymowę, definicję i tłumaczenie
- Ocen siebie: "Znam" lub "Nie znam"
- Aplikacja zapamiętuje twoje błędy i częściej pokazuje trudne słówka
- Twój postęp jest automatycznie zapisywany

### Parsery - Konwersja PDF → JSON

Jeśli masz PDF-y z podręcznikami, możesz je sparsować na JSON.

#### Master Parser (główny interfejs)

```bash
python master_parser.py
```

Wybierz opcję:
1. **New Enterprise** - Parsuj PDF-y z tej serii
2. **English File** - Parsuj PDF-y z tej serii
3. **FULL AUTO** - Parsuj wszystkie PDF-y automatycznie
4. **Wyjście**

#### Parser New Enterprise

```bash
# Tryb interaktywny (pytania dla każdego wpisu)
python parsers/new_enterprise_parser.py

# Tryb w pełni automatyczny
python parsers/new_enterprise_parser.py --full-auto
```

Wyniki zapisywane w: `data/new_enterprise/json/`

#### Parser English File

```bash
# Tryb w pełni automatyczny (domyślny)
python parsers/english_file_parser.py --full-auto
```

Wyniki zapisywane w: `data/english_file/json/`

## 📁 Struktura katalogów

```
fiszki/
├── flashcard_app.py           # Główna aplikacja
├── master_parser.py           # Interfejs do parserów
├── CHANGELOG.md               # Historia zmian
├── README.md                  # Ten plik
│
├── data/
│   ├── new_enterprise/
│   │   ├── pdf/              # Dodaj tu PDF-y New Enterprise
│   │   └── json/             # Parsowane pliki (automatycznie generowane)
│   │       ├── *_parsed.json
│   │       └── ...
│   │
│   └── english_file/
│       ├── pdf/              # Dodaj tu PDF-y English File
│       └── json/             # Parsowane pliki (automatycznie generowane)
│           ├── *_parsed.json
│           └── ...
│
└── parsers/
    ├── new_enterprise_parser.py   # Parser dla New Enterprise
    └── english_file_parser.py     # Parser dla English File
```

## 📄 Format danych JSON

Aplikacja pracuje z JSON-ami o strukturze:

```json
[
  {
    "word": "hello",
    "pronunciation": "həˈləʊ",
    "part_of_speech": "n",
    "definition": "a greeting or polite word",
    "translation": "cześć",
    "unit": "1a",
    "page": 5,
    "correct_count": 3,
    "wrong_count": 1
  },
  ...
]
```

### Wymagane pola:
- **word** - słowo do nauki
- **unit** - dział/jednostka (np. "1a", "Unit 1")
- **correct_count** - liczba poprawnych odpowiedzi (start: 0)
- **wrong_count** - liczba błędnych odpowiedzi (start: 0)

### Pola opcjonalne:
- **pronunciation** - wymowa (IPA lub inna notacja)
- **part_of_speech** - część mowy (n=noun, v=verb, adj=adjective, etc.)
- **definition** - definicja angielska
- **translation** - tłumaczenie na polski
- **page** - strona w podręczniku

## 🎓 System powtórek

Słówka, które sprawiają ci trudności, pojawiają się częściej:

```
waga = max(1, 10 + (błędy × 2) - poprawne)
```

**Przykłady:**
- Nowe słówko (0 poprawnych, 0 błędów) → waga = 10
- Złe słówko (0 poprawnych, 5 błędów) → waga = 20
- Dobrze znane słówko (10 poprawnych, 1 błąd) → waga = 1

## 🔧 Rozwiązywanie problemów

### Problem: "Brak serii" przy uruchomieniu aplikacji

**Przyczyna:** Brak plików JSON w folderach danych

**Rozwiązanie:**
1. Dodaj PDF-y do `data/new_enterprise/pdf/` lub `data/english_file/pdf/`
2. Uruchom `python master_parser.py` lub bezpośrednio parser
3. Parser wygeneruje pliki JSON

### Problem: Parser nie znajduje PDF-ów

**Przyczyna:** Złe lokalizacje folderów

**Rozwiązanie:**
- Upewnij się, że struktura katalogów jest poprawna
- PDF-y muszą być w folderze `.../data/<seria>/pdf/`
- Parser automatycznie skanuje poprawne lokalizacje

### Problem: "ModuleNotFoundError: No module named 'fitz'"

**Rozwiązanie:**
```bash
pip install PyMuPDF
```

### Problem: Znaki diakrytyczne źle wyświetlają się

**Przyczyna:** Encoding

**Rozwiązanie:**
- Upewnij się, że JSON-y są zapisane z kodowaniem UTF-8 (domyślnie dla parserów)
- Parsery automatycznie używają UTF-8

### Problem: Aplikacja nie ładuje się

**Przyczyna:** Brakuje Tkinter

**Rozwiązanie:**
- Na Windows: Tkinter powinien być zainstalowany z Pythonem, spróbuj przeinstalować Python zaznaczając TCL/TK
- Na Linux: `sudo apt-get install python3-tk`
- Na macOS: Tkinter powinien być domyślnie

## 📊 Jak działa parsowanie PDF-ów?

### New Enterprise

Format w PDF-ach:
```
word \ pronunciation \ (part_of_speech) = definition
```

**Przykład:**
```
hello \ həˈləʊ \ (n) = greeting
```

Parser:
1. Skanuje strony w poszukiwaniu "Unit X"
2. Szuka wpisów ze backslashami (`\`)
3. Ekstrahuje słowo, wymowę, część mowy, definicję
4. Zapisuje do JSON-a

### English File

Format w PDF-ach:
```
word part_of_speech /pronunciation/ definition translation
```

**Przykład:**
```
hello n /həˈləʊ/ greeting cześć
```

Parser:
1. Skanuje strony w poszukiwaniu "File X"
2. Zbiera kolejne linie (definicje mogą być złamane)
3. Parsuje za pomocą regex-ów
4. Zapisuje do JSON-a

## 💾 Zapisywanie postępu

Postęp jest automatycznie zapisywany do pliku JSON po każdej odpowiedzi.  
Pola `correct_count` i `wrong_count` są aktualizowane.

Możesz edytować ręcznie:
```json
{
  "word": "hello",
  "correct_count": 0,
  "wrong_count": 0
}
```

Lub resetować postęp z poziomu aplikacji.

## 🐛 Raportowanie błędów

Jeśli parser źle paruje słówka:
1. Sprawdź format w PDF-ie
2. Spróbuj trybu ręcznego: `python parsers/new_enterprise_parser.py`
3. Potwierdzaj/odrzucaj wpisy manualnie

## 📝 Licencja

Projekt otwarty. Użyj swobodnie.

## 👤 Autor

Wojciech Halasa

---

**Wersja:** 3.0  
**Ostatnia aktualizacja:** Styczeń 29, 2026  
**Status:** W pełni funkcjonalny ✅
