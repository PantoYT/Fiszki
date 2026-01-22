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

doc = fitz.open(pdf_path)
print(f"Parsowanie {len(doc)} stron...\n")

all_words = []
current_unit = "Unknown"

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    lines = text.split('\n')
    
    for line in lines:
        unit_match = re.search(r'Unit\s+\d+.*?(\d+[a-z])\b', line, re.IGNORECASE)
        if unit_match:
            current_unit = unit_match.group(1)
            print(f"[Strona {page_num}] Znaleziono jednostkę: Unit {current_unit}")
            break
        
        standalone_match = re.search(r'\b(\d+[a-z])\b', line)
        if standalone_match and len(line.strip()) < 50:
            potential_unit = standalone_match.group(1)
            if not re.search(r'(st|nd|rd|th)', line):
                current_unit = potential_unit
                print(f"[Strona {page_num}] Znaleziono jednostkę: Unit {current_unit}")
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
                if next_line and not next_line.isdigit():
                    full_entry += " " + next_line
                i += 1
            
            try:
                word_match = re.match(r'^([^\\\s(]+)', full_entry)
                if not word_match:
                    continue
                word = word_match.group(1).strip()
                
                phon_match = re.search(r'\\([^\\]+)\\', full_entry)
                pronunciation = phon_match.group(1).strip() if phon_match else ""
                
                pos_match = re.search(r'\(([^)]+)\)', full_entry)
                part_of_speech = pos_match.group(1).strip() if pos_match else ""
                
                def_match = re.search(r'=\s*(.+)', full_entry)
                definition = def_match.group(1).strip() if def_match else ""
                
                all_words.append({
                    "word": word,
                    "pronunciation": pronunciation,
                    "part_of_speech": part_of_speech,
                    "definition": definition,
                    "unit": current_unit,
                    "page": page_num,
                    "correct_count": 0,
                    "wrong_count": 0
                })
                
                print(f"Sparsowano: {word} (Unit {current_unit})")
                
            except Exception as e:
                print(f"Blad: {full_entry[:50]}... - {e}")
        else:
            i += 1

print(f"\nSparsowano {len(all_words)} słówek")

# Grupuj słówka według jednostek
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

print(f"\nZapisano do: {output_path}")