import fitz
import os
import json
import re
import sys

def get_data_dirs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    series_dir = os.path.join(project_root, "data", "new_enterprise")
    pdf_dir = os.path.join(series_dir, "pdf")
    json_dir = os.path.join(series_dir, "json")
    return pdf_dir, json_dir

def parse_pdf(pdf_path, auto_mode=True):
    doc = fitz.open(pdf_path)
    print(f"\nParsowanie {len(doc)} stron z {os.path.basename(pdf_path)}...")
    
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
                print(f"  [Strona {page_num + 1}] Jednostka: Unit {current_unit}")
                break
            
            standalone_match = re.search(r'^\s*(\d+[a-z])\s*$', line)
            if standalone_match:
                current_unit = standalone_match.group(1)
                print(f"  [Strona {page_num + 1}] Jednostka: Unit {current_unit}")
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
                    else:
                        print(f"\n--- Znaleziono wpis ---")
                        print(f"Slowo: {word}")
                        print(f"Wymowa: {pronunciation}")
                        print(f"Czesc mowy: {part_of_speech}")
                        print(f"Definicja: {definition[:100]}{'...' if len(definition) > 100 else ''}")
                        print(f"Jednostka: {current_unit}")
                        
                        while True:
                            confirm = input("\nDodac? (t/n/q): ").lower()
                            if confirm == 't':
                                all_words.append(entry)
                                print(f"Dodano: {word}")
                                break
                            elif confirm == 'n':
                                skipped_count += 1
                                print(f"Pominieto: {word}")
                                break
                            elif confirm == 'q':
                                return all_words, skipped_count, True
                            else:
                                print("Wpisz 't', 'n' lub 'q'")
                    
                except Exception as e:
                    if not auto_mode:
                        print(f"\nBlad: {full_entry[:100]}... - {e}")
                        input("Enter aby kontynuowac...")
            else:
                i += 1
    
    return all_words, skipped_count, False

def main():
    full_auto = "--full-auto" in sys.argv
    
    pdf_dir, json_dir = get_data_dirs()
    
    if not os.path.exists(pdf_dir):
        print("Folder pdf/ nie istnieje!")
        return
    
    os.makedirs(json_dir, exist_ok=True)
    
    pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
    
    if not pdf_files:
        print("Brak plikow PDF!")
        return
    
    if full_auto:
        print("\n" + "="*60)
        print("NEW ENTERPRISE - FULL AUTO")
        print("="*60)
        print(f"\nZnaleziono {len(pdf_files)} plikow PDF")
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_dir, pdf_file)
            words, _, _ = parse_pdf(pdf_path, auto_mode=True)
            
            output_filename = f"{os.path.splitext(pdf_file)[0]}_parsed.json"
            output_path = os.path.join(json_dir, output_filename)
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(words, f, ensure_ascii=False, indent=2)
            
            print(f"  {pdf_file}: {len(words)} slowek -> {output_filename}")
        
        print(f"\n{'='*60}")
        print("Zakonczono parsowanie wszystkich plikow!")
        print(f"{'='*60}")
    else:
        print("Dostepne podreczniki New Enterprise:")
        for idx, pdf_file in enumerate(pdf_files, 1):
            print(f"{idx}. {pdf_file}")
        
        while True:
            try:
                choice = int(input("\nWybierz numer (0=wyjscie): "))
                if choice == 0:
                    print("Anulowano.")
                    return
                if 1 <= choice <= len(pdf_files):
                    selected_pdf = pdf_files[choice - 1]
                    break
                else:
                    print("Nieprawidlowy numer.")
            except ValueError:
                print("Wprowadz liczbe.")
        
        pdf_path = os.path.join(pdf_dir, selected_pdf)
        print(f"\nWybrano: {selected_pdf}")
        
        print("\n1. Automatyczny\n2. Reczny")
        while True:
            try:
                mode = int(input("Tryb: "))
                if mode in [1, 2]:
                    auto_mode = (mode == 1)
                    break
            except ValueError:
                pass
        
        words, skipped, interrupted = parse_pdf(pdf_path, auto_mode)
        
        if interrupted:
            print("\nPrzerwano.")
            return
        
        print(f"\n{'='*60}")
        print(f"Sparsowano: {len(words)} slowek")
        if skipped > 0:
            print(f"Pominieto: {skipped}")
        
        units_summary = {}
        for word in words:
            unit = word['unit']
            units_summary[unit] = units_summary.get(unit, 0) + 1
        
        print("\nPodsumowanie jednostek:")
        for unit, count in sorted(units_summary.items()):
            print(f"  Unit {unit}: {count} slowek")
        
        output_filename = f"{os.path.splitext(selected_pdf)[0]}_parsed.json"
        output_path = os.path.join(json_dir, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False, indent=2)
        
        print(f"\nZapisano: {output_path}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrzerwano.")