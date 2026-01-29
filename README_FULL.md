# Fiszki - Pełna Dokumentacja

> Dla tych którzy nie umieją w języki, dla kotków i piesków 🐱🐶

Offline'owa aplikacja desktopowa do nauki słownictwa z plików PDF poprzez inteligentne parsowanie.

## 📚 Dostępne źródła

### Oficjalne źródła książek

| Seria | Zasoby |
|------|---------|
| **Career Paths** | https://learningclub.egis.com.pl/pl/angielskizawodowy |
| **English File** | https://docer.pl/doc/x15cv5v |
| **New Enterprise** | https://vipclub.egis.com.pl/pl/szkolasrednia/newenterprise |

### Alternatywne źródła

- **Wayback Machine** - `archive.org/web/` → PDF export
- **Wyszukaj**: `wordlist`, `glossary`, `wortschatz`, itp.

## 📖 Instrukcja obsługi

### Aplikacja (flashcard_app.py)

1. **Wybierz podręcznik** - Kliknij "Wybierz podręcznik" aby wybrać serię
2. **Wybierz poziom** - Zaznacz plik z konkretnym poziomem (A1, A2, B1, etc.)
3. **Wybierz działy** - Zaznacz które działy chcesz powtarzać
4. **Rozpocznij naukę** - Kliknij "Start" aby rozpocząć sesję

**Podczas nauki:**
- Przeczytaj słówko na karcie
- SPACE - przewróć kartę aby zobaczyć wymowę, definicję i tłumaczenie
- LEFT arrow - nie znam (błąd)
- RIGHT arrow - znam (OK)
- Aplikacja zapamiętuje twoje błędy i częściej pokazuje trudne słówka
- Twój postęp jest automatycznie zapisywany

### Parsery - Konwersja PDF → JSON

#### Master Parser (główny interfejs)

```bash
python parsers/master_parser.py
```

Wybierz opcję:
1. **New Enterprise** - Parsuj PDF-y z tej serii
2. **English File** - Parsuj PDF-y z tej serii
3. **Career Paths** - Parsuj PDF-y z tej serii
4. **FULL AUTO** - Parsuj wszystkie PDF-y automatycznie
5. **Wyjście**

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

#### Parser Career Paths

```bash
# Tryb w pełni automatyczny - skanuje wszystkie kategorie
python parsers/career_paths_parser.py --full-auto
```

Wyniki zapisywane w: `data/career_paths/<kategoria>/json/`

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
  }
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
2. Uruchom `python parsers/master_parser.py` lub bezpośrednio parser
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
pip install -r requirements.txt
```

### Problem: Znaki diakrytyczne źle wyświetlają się

**Przyczyna:** Encoding

**Rozwiązanie:**
- Upewnij się, że JSON-y są zapisane z kodowaniem UTF-8
- Parsery automatycznie używają UTF-8

### Problem: Aplikacja nie ładuje się

**Przyczyna:** Brakuje Tkinter

**Rozwiązanie:**
- Na Windows: Tkinter powinien być zainstalowany z Pythonem
- Na Linux: `sudo apt-get install python3-tk`
- Na macOS: Tkinter powinien być domyślnie

## 📊 Jak działa parsowanie PDF-ów?

### New Enterprise

Format w PDF-ach:
```
word \ pronunciation \ (part_of_speech) = definition
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

Parser:
1. Skanuje strony w poszukiwaniu "File X"
2. Zbiera kolejne linie (definicje mogą być złamane)
3. Parsuje za pomocą regex-ów
4. Zapisuje do JSON-a

### Career Paths

Format w PDF-ach:
```
word [PART_OF_SPEECH-UNIT] definition
```

Parser:
1. Skanuje wszystkie kategorie automatycznie
2. Szuka wpisów w formacie `word [POS-UNIT] definition`
3. Ekstrahuje słowo, część mowy, unit, definicję
4. Zapisuje do JSON-a osobno dla każdej kategorii

## 💾 Zapisywanie postępu

Postęp jest automatycznie zapisywany do pliku JSON po każdej odpowiedzi.  
Pola `correct_count` i `wrong_count` są aktualizowane.

## 📝 Licencja

Projekt otwarty. Użyj swobodnie.

## 👤 Autor

Wojciech Halasa

---

**Wersja:** 4.0
