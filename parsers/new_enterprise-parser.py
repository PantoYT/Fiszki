import fitz
import os
import json
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
pdf_path = os.path.join(project_root, "data", "new_enterprise_b1plus_wordlist_pl.pdf")

doc = fitz.open(pdf_path)
print(f"Parsowanie {len(doc)} stron...\n")

all_words = []

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    lines = text.split('\n')
    
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
                word_match = re.match(r'^([^\\\s]+)\s*\\', full_entry)
                if not word_match:
                    continue
                word = word_match.group(1)
                
                phon_match = re.search(r'\\([^\\]+)\\', full_entry)
                pronunciation = phon_match.group(1) if phon_match else ""
                
                pos_match = re.search(r'\(([^)]+)\)', full_entry)
                part_of_speech = pos_match.group(1) if pos_match else ""
                
                def_match = re.search(r'=\s*(.+)', full_entry)
                definition = def_match.group(1).strip() if def_match else ""
                
                all_words.append({
                    "word": word,
                    "pronunciation": pronunciation,
                    "part_of_speech": part_of_speech,
                    "definition": definition,
                    "page": page_num
                })
                
                print(f"Sparsowano: {word}")
                
            except Exception as e:
                print(f"Blad: {full_entry[:50]}... - {e}")
        else:
            i += 1

print(f"\nSparsowano {len(all_words)} slowek")

output_path = os.path.join(project_root, "data", "parsed_words.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_words, f, ensure_ascii=False, indent=2)

print(f"Zapisano do: {output_path}")