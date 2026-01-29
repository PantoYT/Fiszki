"""
New Enterprise Parser
Parsuje PDF-y z serii New Enterprise i konwertuje je do formatu JSON.
Obsługuje format ze słowami oddzielonymi backslashami.
"""

import fitz  # PyMuPDF
import os
import json
import re
import sys


def get_data_dirs():
    """Pobiera ścieżki do folderów PDF i JSON."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    series_dir = os.path.join(project_root, "data", "new_enterprise")
    pdf_dir = os.path.join(series_dir, "pdf")
    json_dir = os.path.join(series_dir, "json")
    return pdf_dir, json_dir


def parse_pdf(pdf_path, auto_mode=True):
    """
    Parsuje PDF i ekstrahuje słówka.
    
    Format: word \ pronunciation \ (part of speech) definition
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Błąd: Nie można otworzyć {pdf_path}: {e}")
        return [], 0, False
    
    print(f"Parsowanie {len(doc)} stron z {os.path.basename(pdf_path)}...")
    
    all_words = []
    current_unit = "Unknown"
    skipped_count = 0
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        lines = text.split('\n')
        
        # Szukaj jednostki na tej stronie
        for line in lines:
            # Szukaj "Unit 1a" lub podobnych
            unit_match = re.search(r'^Unit\s+\d+[^\d]*?(\d+[a-z])\b', line, re.IGNORECASE)
            if unit_match:
                current_unit = unit_match.group(1)
                break
            
            # Szukaj samodzielnego "1a"
            standalone_match = re.search(r'^\s*(\d+[a-z])\s*$', line)
            if standalone_match:
                current_unit = standalone_match.group(1)
                break
        
        # Parsuj wpisy na tej stronie
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Szukaj wpisu ze slashami: word \ pronunciation \ (POS) = definition
            if '\\' in line and line.count('\\') >= 2:
                full_entry = line
                i += 1
                
                # Zbierz kolejne linie aż do następnego wpisu
                while i < len(lines):
                    next_line = lines[i].strip()
                    
                    # Zakończ jeśli natrafisz na kolejny wpis
                    if '\\' in next_line and next_line.count('\\') >= 2:
                        break
                    
                    # Pomiń puste linie
                    if not next_line:
                        i += 1
                        break
                    
                    # Pomiń numery
                    if next_line.isdigit() and len(next_line) <= 3:
                        i += 1
                        continue
                    
                    # Zakończ jeśli natrafisz na jednostkę
                    if re.search(r'^\s*(\d+[a-z])\s*$', next_line):
                        break
                    
                    full_entry += " " + next_line
                    i += 1
                
                try:
                    # Usuń numer jednostki na końcu (jeśli jest)
                    full_entry = re.sub(r'\s+\d+[a-z]\s*$', '', full_entry)
                    
                    # Ekstrahuj słowo
                    word_match = re.match(r'^([^\\\(]+?)(?=\s*\\)', full_entry)
                    if not word_match:
                        continue
                    
                    word = word_match.group(1).strip()
                    if not word:
                        continue
                    
                    # Ekstrahuj wymowę
                    phon_match = re.search(r'\\([^\\]+)\\', full_entry)
                    pronunciation = phon_match.group(1).strip() if phon_match else ""
                    
                    # Ekstrahuj część mowy
                    pos_match = re.search(r'\\\s*\(([^)]+)\)', full_entry)
                    if not pos_match:
                        pos_match = re.search(r'\\\s*((?:phr\s+)?[a-z]+)\s+(?:=|\()', full_entry)
                    part_of_speech = pos_match.group(1).strip() if pos_match else ""
                    
                    # Ekstrahuj definicję
                    def_match = re.search(r'=\s*(.+)', full_entry)
                    definition = def_match.group(1).strip() if def_match else ""
                    
                    # Wyczyść definicję
                    definition = re.sub(r'\s+\d+[a-z]\s*$', '', definition)
                    definition = definition.strip()
                    
                    entry = {
                        "word": word,
                        "pronunciation": pronunciation,
                        "part_of_speech": part_of_speech,
                        "definition": definition,
                        "unit": current_unit,
                        "page": page_num + 1,
                        "correct_count": 0,
                        "wrong_count": 0
                    }
                    
                    if auto_mode:
                        all_words.append(entry)
                    else:
                        # Tryb ręczny - pytaj użytkownika
                        print(f"\n--- Znaleziono wpis ---")
                        print(f"Słowo: {word}")
                        print(f"Wymowa: {pronunciation}")
                        print(f"Część mowy: {part_of_speech}")
                        print(f"Definicja: {definition[:100]}{'...' if len(definition) > 100 else ''}")
                        print(f"Jednostka: {current_unit}")
                        
                        while True:
                            confirm = input("\nDodać? (t/n/q): ").lower()
                            if confirm == 't':
                                all_words.append(entry)
                                print(f"✓ Dodano: {word}")
                                break
                            elif confirm == 'n':
                                skipped_count += 1
                                print(f"✗ Pominięto: {word}")
                                break
                            elif confirm == 'q':
                                return all_words, skipped_count, True
                            else:
                                print("Wpisz 't', 'n' lub 'q'")
                
                except Exception as e:
                    if not auto_mode:
                        print(f"\nBłąd: {full_entry[:100]}... - {e}")
                        input("Enter aby kontynuować...")
            else:
                i += 1
    
    doc.close()
    return all_words, skipped_count, False



def main():
    """Główna funkcja parsera."""
    full_auto = "--full-auto" in sys.argv
    
    pdf_dir, json_dir = get_data_dirs()
    
    if not os.path.exists(pdf_dir):
        print(f"Błąd: Folder {pdf_dir} nie istnieje!")
        return
    
    os.makedirs(json_dir, exist_ok=True)
    
    pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
    
    if not pdf_files:
        print(f"Błąd: Brak plików PDF w {pdf_dir}")
        return
    
    if full_auto:
        # Tryb full auto - parsuj wszystkie pliki
        print("\n" + "="*70)
        print("NEW ENTERPRISE - FULL AUTO MODE")
        print("="*70)
        print(f"\nZnaleziono {len(pdf_files)} plików PDF\n")
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_dir, pdf_file)
            words, _, _ = parse_pdf(pdf_path, auto_mode=True)
            
            output_filename = f"{os.path.splitext(pdf_file)[0]}_parsed.json"
            output_path = os.path.join(json_dir, output_filename)
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(words, f, ensure_ascii=False, indent=2)
            
            print(f"  ✓ {pdf_file}")
            print(f"    → {len(words)} słówek -> {output_filename}")
        
        print(f"\n{'='*70}")
        print("Ukończono parsowanie wszystkich plików!")
        print(f"{'='*70}\n")
    else:
        # Tryb interaktywny
        print("\nDostępne podręczniki New Enterprise:")
        for idx, pdf_file in enumerate(pdf_files, 1):
            print(f"{idx}. {pdf_file}")
        
        while True:
            try:
                choice = int(input("\nWybierz numer (0=wyjście): "))
                if choice == 0:
                    print("Anulowano.")
                    return
                if 1 <= choice <= len(pdf_files):
                    selected_pdf = pdf_files[choice - 1]
                    break
                else:
                    print("Nieprawidłowy numer.")
            except ValueError:
                print("Wprowadź liczbę.")
        
        pdf_path = os.path.join(pdf_dir, selected_pdf)
        print(f"\nWybrano: {selected_pdf}")
        
        print("\nWybierz tryb:")
        print("1. Automatyczny (bez potwierdzania)")
        print("2. Ręczny (potwierdzenie każdego wpisu)")
        
        while True:
            try:
                mode = int(input("\nTryb (1 lub 2): "))
                if mode in [1, 2]:
                    auto_mode = (mode == 1)
                    break
                else:
                    print("Wybierz 1 lub 2")
            except ValueError:
                print("Wprowadź liczbę.")
        
        words, skipped, interrupted = parse_pdf(pdf_path, auto_mode)
        
        if interrupted:
            print("\nPrzerwano.")
            return
        
        print(f"\n{'='*70}")
        print("Podsumowanie")
        print(f"{'='*70}")
        print(f"Sparsowano: {len(words)} słówek")
        if skipped > 0:
            print(f"Pominięto: {skipped} wpisów")
        
        units_summary = {}
        for word in words:
            unit = word['unit']
            units_summary[unit] = units_summary.get(unit, 0) + 1
        
        print("\nRozkład na jednostki:")
        for unit in sorted(units_summary.keys()):
            count = units_summary[unit]
            print(f"  Unit {unit}: {count} słówek")
        
        output_filename = f"{os.path.splitext(selected_pdf)[0]}_parsed.json"
        output_path = os.path.join(json_dir, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Zapisano: {output_path}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrzerwano.")
        sys.exit(1)