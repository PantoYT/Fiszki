# Changelog

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