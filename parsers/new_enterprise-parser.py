import fitz
import os
import json
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_dir = os.path.join(project_root, "data")

pdf_files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]

if not pdf_files:
    print("Nie znaleziono plików PDF w folderze data/")
    exit()

print("Dostępne podręczniki:")
for idx, pdf_file in enumerate(pdf_files, 1):
    print(f"{idx}. {pdf_file}")

while True:
    try:
        choice = int(input("\nWybierz numer podręcznika (lub 0 aby wyjść): "))
        if choice == 0:
            print("Anulowano.")
            exit()
        if 1 <= choice <= len(pdf_files):
            selected_pdf = pdf_files[choice - 1]
            break
        else:
            print("Nieprawidłowy numer. Spróbuj ponownie.")
    except ValueError:
        print("Wprowadź poprawną liczbę.")

pdf_path = os.path.join(data_dir, selected_pdf)
print(f"\nWybrano: {selected_pdf}")

print("\nWybierz tryb parsowania:")
print("1. Automatyczny (parsowanie bez potwierdzenia)")
print("2. Ręczny (potwierdzenie każdego wpisu)")

while True:
    try:
        mode = int(input("Wybierz tryb (1 lub 2): "))
        if mode in [1, 2]:
            auto_mode = (mode == 1)
            break
        else:
            print("Nieprawidłowy wybór. Wybierz 1 lub 2.")
    except ValueError:
        print("Wprowadź poprawną liczbę.")

doc = fitz.open(pdf_path)
print(f"\nParsowanie {len(doc)} stron...\n")

all_words = []
current_unit = "Unknown"
skipped_count = 0

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    lines = text.split('\n')
    
    for line in lines:
        unit_match = re.search(r'^Unit\s+\d+[^\d]*?(\d+[a-z])\b', line, re.IGNORECASE)
        if unit_match:
            current_unit = unit_match.group(1)
            print(f"\n[Strona {page_num + 1}] Znaleziono jednostkę: Unit {current_unit}\n")
            break
        
        standalone_match = re.search(r'^\s*(\d+[a-z])\s*$', line)
        if standalone_match:
            current_unit = standalone_match.group(1)
            print(f"\n[Strona {page_num + 1}] Znaleziono jednostkę: Unit {current_unit}\n")
            break
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if '\\' in line and line.count('\\') >= 2:
            full_entry = line
            i += 1
            
            while i < len(lines):
                next_line = lines[i].strip()
                
                if '\\' in next_line and next_line.count('\\') >= 2:
                    break
                
                if not next_line:
                    i += 1
                    break
                
                if next_line.isdigit() and len(next_line) <= 3:
                    i += 1
                    continue
                
                if re.search(r'^\s*(\d+[a-z])\s*$', next_line):
                    break
                
                full_entry += " " + next_line
                i += 1
            
            try:
                full_entry = re.sub(r'\s+\d+[a-z]\s*$', '', full_entry)
                
                word_match = re.match(r'^([^\\\(]+?)(?=\s*\\)', full_entry)
                if not word_match:
                    continue
                    
                word = word_match.group(1).strip()
                
                phon_match = re.search(r'\\([^\\]+)\\', full_entry)
                pronunciation = phon_match.group(1).strip() if phon_match else ""
                
                pos_match = re.search(r'\\\s*\(([^)]+)\)', full_entry)
                if not pos_match:
                    pos_match = re.search(r'\\\s*((?:phr\s+)?[a-z]+)\s+(?:=|\()', full_entry)
                part_of_speech = pos_match.group(1).strip() if pos_match else ""
                
                def_match = re.search(r'=\s*(.+)', full_entry)
                definition = def_match.group(1).strip() if def_match else ""
                
                definition = re.sub(r'\s+\d+[a-z]\s*$', '', definition)
                
                entry = {
                    "word": word,
                    "pronunciation": pronunciation,
                    "part_of_speech": part_of_speech,
                    "definition": definition,
                    "unit": current_unit,
                    "page": page_num,
                    "correct_count": 0,
                    "wrong_count": 0
                }
                
                if auto_mode:
                    all_words.append(entry)
                    print(f"✓ {word} ({part_of_speech}) - Unit {current_unit}")
                else:
                    print(f"\n--- Znaleziono wpis ---")
                    print(f"Słowo: {word}")
                    print(f"Wymowa: {pronunciation}")
                    print(f"Część mowy: {part_of_speech}")
                    print(f"Definicja: {definition[:100]}{'...' if len(definition) > 100 else ''}")
                    print(f"Jednostka: {current_unit}")
                    
                    while True:
                        confirm = input("\nDodać ten wpis? (t/n/q=zakończ): ").lower()
                        if confirm == 't':
                            all_words.append(entry)
                            print(f"✓ Dodano: {word}")
                            break
                        elif confirm == 'n':
                            skipped_count += 1
                            print(f"✗ Pominięto: {word}")
                            break
                        elif confirm == 'q':
                            print("\nZakończono parsowanie.")
                            break
                        else:
                            print("Wpisz 't' (tak), 'n' (nie) lub 'q' (zakończ)")
                    
                    if confirm == 'q':
                        break
                
            except Exception as e:
                print(f"\n⚠ Błąd parsowania: {full_entry[:100]}...")
                print(f"   Szczegóły: {e}")
                if not auto_mode:
                    input("Naciśnij Enter aby kontynuować...")
        else:
            i += 1
    
    if not auto_mode and i < len(lines):
        break

print(f"\n{'='*60}")
print(f"Parsowanie zakończone!")
print(f"{'='*60}")
print(f"Sparsowano: {len(all_words)} słówek")
if not auto_mode and skipped_count > 0:
    print(f"Pominięto: {skipped_count} wpisów")

units_summary = {}
for word in all_words:
    unit = word['unit']
    if unit not in units_summary:
        units_summary[unit] = 0
    units_summary[unit] += 1

print("\nPodsumowanie jednostek:")
for unit, count in sorted(units_summary.items()):
    print(f"  Unit {unit}: {count} słówek")

pdf_name_without_ext = os.path.splitext(selected_pdf)[0]
output_filename = f"{pdf_name_without_ext}_parsed.json"
output_path = os.path.join(data_dir, output_filename)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_words, f, ensure_ascii=False, indent=2)

print(f"\n✓ Zapisano do: {output_path}")