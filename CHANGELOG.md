# Changelog

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