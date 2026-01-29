# Fiszki

Prosta aplikacja desktopowa do nauki słownictwa z plików JSON.  
Offline, bez kont, bez śledzenia, bez rozpraszaczy.

Projekt opiera się na założeniu, że **każdy podręcznik posiada jednolity (uniform) format listy słówek**.  
Parsery nie próbują „rozumieć PDF-a jako całości”, tylko **wydobywają tekst i parsują powtarzalne wzorce wpisów charakterystyczne dla danej serii**.

---

## 🚀 Funkcje

- Nauka słownictwa w formie fiszek  
- Tryb offline  
- Brak kont i logowania  
- System powtórek oparty o liczbę błędów  
- Obsługa wielu serii podręczników  
- Parsery PDF (opcjonalne, jednorazowe)

---

## 🧩 Wymagania

- Python **3.10+**
- Tkinter (zazwyczaj w standardowej dystrybucji Pythona)
- PyMuPDF (`pip install PyMuPDF`) – **tylko jeśli używasz parserów PDF**

---

## 📦 Instalacja

```bash
git clone <repo-url>
cd fiszki
python flashcard_app.py

## 📁 Struktura katalogów

fiszki/
├── flashcard_app.py          # Główna aplikacja
├── data/
│   ├── new_enterprise/
│   │   ├── pdf/              # PDF-y (opcjonalne)
│   │   └── json/             # *_parsed.json
│   └── english_file/
│       ├── pdf/
│       └── json/
├── parsers/
│   ├── master_parser.py
│   ├── new_enterprise_parser.py
│   └── english_file_parser.py
└── README.md

## 📄 Format danych (JSON)

Aplikacja nie czyta PDF-ów bezpośrednio.
Źródłem danych są pliki JSON o ujednoliconej strukturze:

[
  {
    "word": "hello",
    "pronunciation": "həˈləʊ",
    "part_of_speech": "n",
    "definition": "a greeting",
    "unit": "1a",
    "page": 5,
    "correct_count": 0,
    "wrong_count": 0
  }
]

Wymagane pola

word – słowo do nauki

unit – dział / lekcja

correct_count – liczba poprawnych odpowiedzi

wrong_count – liczba błędnych odpowiedzi

Pola opcjonalne

pronunciation / phonetic

part_of_speech

definition

translation

page

Parser może zostawić pola opcjonalne puste – aplikacja to obsługuje.

## 🔁 System wagowy (powtórki)

Słówka, na których częściej popełniasz błędy, pojawiają się częściej:

waga = max(1, 10 + (wrong_count * 2) - correct_count)

## 📄 Parsery PDF (opcjonalne)

Parsery służą wyłącznie do jednorazowej konwersji PDF → JSON.

Parser:

nie jest uniwersalny dla wszystkich PDF-ów,

jest pisany pod konkretną serię podręczników,

zakłada powtarzalny wzorzec wpisów.

Proces działania:

PDF → tekst (PyMuPDF)

Normalizacja tekstu (łączenie łamanych linii)

Dopasowanie wzorca wpisu (regex)

## 📚 Wspierane serie

New Enterprise

Format wpisu:

word \pronunciation\ (pos) = definition


Parser: parsers/new_enterprise_parser.py

wykrywa jednostki (np. Unit 1a, 2b)

obsługuje tryb automatyczny i ręczny

zapisuje dane zgodnie z formatem aplikacji

English File

Format wpisu (elastyczny):

word [part_of_speech] [/phonetic/] definition


Parser: parsers/english_file_parser.py

nie zakłada poziomu (Elementary–Advanced)

toleruje brak fonetyki i części mowy

parsuje wzorzec językowy, nie layout strony

działa na podstawie jednolitej listy słówek

## ▶️ Użycie parserów

Interaktywnie
python parsers/master_parser.py

Full auto (wszystkie PDF-y w serii)
python parsers/english_file_parser.py --full-auto
python parsers/new_enterprise_parser.py --full-auto


Parser zapisze pliki do:

data/<seria>/json/*_parsed.json

## 🧠 Master parser

master_parser.py:

wykrywa dostępne serie

uruchamia odpowiednie parsery

umożliwia parsowanie wielu serii jednym poleceniem

## 🛠️ Troubleshooting
Parser zwraca 0 słówek

PDF:

nie zawiera listy słówek w oczekiwanym formacie, lub

ma inny wzorzec wpisu niż założony w parserze

Brak wyników nie jest błędem wykonania.

PDF jest skanem

PyMuPDF nie zwróci tekstu

wymagany OCR (poza zakresem projektu)

Seria nie pojawia się w aplikacji

sprawdź, czy istnieje data/<seria>/json/

sprawdź poprawność plików JSON

nazwa folderu serii musi być zgodna

## 🔧 Rozszerzanie projektu
Dodanie nowej serii (bez PDF)

Utwórz data/nazwa_serii/json/

Dodaj pliki *_parsed.json

Seria pojawi się automatycznie w aplikacji.

Dodanie nowej serii z PDF

Utwórz data/nazwa_serii/pdf/

Napisz parser parsers/nazwa_serii_parser.py

Dodaj serię do master_parser.py

Parser powinien:

zakładać uniform word list

nie polegać na numerach stron ani layoutcie

parsować wzorzec wpisu, nie wygląd strony

## 🧪 Technologie

Python

Tkinter

JSON

PyMuPDF (parsery PDF)

## 🎯 Dla kogo?

Uczniowie przygotowujący się do egzaminów

Osoby uczące się słownictwa offline

Każdy, kto nie chce kont, reklam i platform online

## 👤 Autor

Wojciech Halasa

Projekt powstał z wykorzystaniem narzędzi GenAI do analizy kodu i konsultacji architektonicznych.
Końcowe decyzje projektowe i implementacja należą do autora.

## 📜 Licencja

MIT