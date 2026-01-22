# Fiszki

**Fiszki** to prosta, lokalna aplikacja desktopowa do nauki słownictwa, napisana w Pythonie z użyciem **Tkintera**.  
Projekt powstał z myślą o realnej nauce – bez kont, bez internetu, bez rozpraszaczy.

Aplikacja wspiera fiszki generowane m.in. z podręczników **New Enterprise** (przez dedykowane parsery) i umożliwia naukę z podziałem na działy (unity).

---

## Funkcje

- nauka słówek w formie fiszek (przód / tył)
- wybór konkretnych działów (unitów)
- losowanie słówek z **wagami**  
  (słówka błędne pojawiają się częściej)
- zapamiętywanie postępów nauki (poprawne / błędne odpowiedzi)
- licznik czasu sesji
- statystyki nauki
- pełna praca **offline**
- czytelny, minimalistyczny interfejs

---

## Dane

Aplikacja korzysta z plików `.json`, które powinny znajdować się w folderze:

```

data/

```

Pliki muszą mieć nazwę kończącą się na:

```

_parsed.json

````

Każdy plik reprezentuje jeden podręcznik lub zestaw fiszek.

---

## Jak uruchomić

### Wersja developerska
1. Zainstaluj Python (3.10+)
2. Sklonuj repozytorium
3. Upewnij się, że folder `data/` istnieje i zawiera pliki JSON
4. Uruchom:
   ```bash
   python main.py

## Dla kogo?

* uczniowie uczący się słownictwa (np. do matury)
* osoby chcące uczyć się **offline**
* każdy, kto woli fiszki bez kont, reklam i algorytmów platform edukacyjnych

---

## Technologie

* Python
* Tkinter (GUI)
* JSON
* losowanie ważone

---

## Autor

**Wojciech Hałasa**

---

## Wsparcie AI

Projekt powstał **z wykorzystaniem wsparcia generatywnej GenAI**
– głównie jako narzędzia do:

* analizy kodu
* poprawy czytelności
* konsultacji architektonicznych

Końcowe decyzje projektowe i implementacja należą do autora.
