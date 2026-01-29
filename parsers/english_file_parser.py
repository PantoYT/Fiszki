"""
English File Parser - v3.5 KOMPLETNIE PROSTO
Najprosztsza możliwa logika:
1. Czytaj aż do polskiego słowa
2. Szukaj wymowy /.../ gdziekolwiek w tekście
3. Ostatnie polskie słowo to translation
"""

import fitz
import os
import json
import glob
import re
import sys


def get_data_dirs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    series_dir = os.path.join(project_root, "data", "english_file")
    pdf_dir = os.path.join(series_dir, "pdf")
    json_dir = os.path.join(series_dir, "json")
    return pdf_dir, json_dir


def extract_text(pdf_path):
    """Ekstrahuje tekst z PDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num, page in enumerate(doc):
            text += f"__PAGE_{page_num+1}__\n"
            text += page.get_text() + "\n"
        doc.close()
        return text
    except Exception as e:
        print(f"ERROR: {e}")
        return ""


def clean_text_line(line):
    """Czyści linię tekstu."""
    line = re.sub(r'\s+', ' ', line)
    return line.strip()


def extract_pronunciation(text):
    """Wyodrębnij wymowę z tekstu - format /.../ """
    match = re.search(r'/([^/]+)/', text)
    if match:
        return match.group(1).strip()
    return ""


def extract_pos(text):
    """Wyodrębnij część mowy: adj, n, v, itp"""
    match = re.search(r'\b(adj|n|v|adv|phr|pron|prep|conj|exc|interj)\b', text, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return ""


def parse_vocabulary_list(text):
    """
    Ultra-prosta strategia:
    Każde angielskie słowo jest wpisem.
    Zbieraj tekst aż do polskiego słowa (zawiera [ąćęłńóśźż])
    """
    
    entries = []
    current_unit = "File 1"
    current_page = 1
    processed_words = set()
    
    lines = text.split('\n')
    
    i = 0
    while i < len(lines):
        raw_line = lines[i].strip()
        i += 1
        
        # Śledź jednostki
        file_match = re.match(r'File\s+(\d+)\s*$', raw_line, re.IGNORECASE)
        if file_match:
            current_unit = f"File {file_match.group(1)}"
            continue
        
        # Śledź strony
        page_match = re.match(r'__PAGE_(\d+)__', raw_line)
        if page_match:
            current_page = int(page_match.group(1))
            continue
        
        line = clean_text_line(raw_line)
        
        if not line or len(line) < 2:
            continue
        
        # Czy zawiera znaki polskie? Skip
        if re.search(r'[ąćęłńóśźż]', line):
            continue
        
        # Czy to słowo angielskie? (mała litera na początku)
        if not re.match(r'^[a-z]', line, re.IGNORECASE):
            continue
        
        # Wyodrębnij pierwsze słowo (to bedzie nasz główny word)
        words = line.split()
        if not words:
            continue
        
        potential_word = words[0]
        
        # Walidacja
        if not potential_word or len(potential_word) < 2 or potential_word.isdigit():
            continue
        
        # Skip nagłówki
        if potential_word.lower() in ["vocabulary", "useful", "words", "phrases", "bank", "english", "file", "upper", "intermediate", "polish", "wordlist"]:
            continue
        
        # Unikaj duplikatów z tej samej jednostki
        dedup_key = (potential_word.lower(), current_unit)
        if dedup_key in processed_words:
            continue
        processed_words.add(dedup_key)
        
        # Wyodrębnij POS i pronunciation z tej linii
        pos = extract_pos(line)
        pronunciation = extract_pronunciation(line)
        
        # Zbierz tekst aż do polskiego słowa
        full_text = line
        
        while i < len(lines):
            next_raw = lines[i].strip()
            next_line = clean_text_line(next_raw)
            
            # Czy zawiera znaki polskie? To koniec wpisu!
            if re.search(r'[ąćęłńóśźż]', next_line):
                full_text += " " + next_line
                i += 1
                break
            
            # Czy to nowe słowo angielskie na początku? (następny wpis)
            if re.match(r'^[a-z][a-z\s\-]*?\s*(?:adj|n|v|adv|phr|pron|prep|conj|exc|interj)?\s*$', 
                       next_line, re.IGNORECASE) and len(next_line.split()[0]) >= 2:
                # To nowe słowo, nie dodawaj
                break
            
            # Czy to File marker?
            if re.match(r'^File\s+\d+', next_line, re.IGNORECASE):
                break
            
            # Dodaj do full_text
            if next_line:
                full_text += " " + next_line
            i += 1
        
        # Teraz parsuj full_text
        # Szukaj wymowy jeśli nie znalazłem wcześniej
        if not pronunciation:
            pronunciation = extract_pronunciation(full_text)
        
        # Szukaj POS jeśli nie znalazłem wcześniej
        if not pos:
            pos = extract_pos(full_text)
        
        # Wyodrębnij translation (ostatnie polskie słowo)
        translation = ""
        polish_words = [w for w in full_text.split() if re.search(r'[ąćęłńóśźż]', w)]
        if polish_words:
            translation = polish_words[-1]
            # Usuń translation z tekstu
            full_text = re.sub(r'\s+' + re.escape(translation) + r'\s*$', '', full_text).strip()
        
        # Usuń wymowę z full_text (będzie w dedykowanym polu)
        definition = re.sub(r'/[^/]+/', '', full_text).strip()
        # Usuń POS z definicji
        definition = re.sub(r'\b(adj|n|v|adv|phr|pron|prep|conj|exc|interj)\b\s*', '', 
                           definition, flags=re.IGNORECASE).strip()
        
        # NOWA LOGIKA: Szukaj zdań zaczynających się wielkimi literami (to są definicje)
        # Format: "Capital Letter sentence ends with a period. translation_word"
        sentences = re.findall(r'[A-Z][^.!?]*[.!?]', definition)
        if sentences:
            # Weź ostatnie zdanie (przed polskim słowem)
            definition = ' '.join(sentences)
            definition = definition.replace(potential_word, '').strip()
        
        # Usuń zduplikowane słowo angielskie z definicji
        definition_words = []
        for word in definition.split():
            if not re.search(re.escape(potential_word), word, re.IGNORECASE):
                definition_words.append(word)
        definition = " ".join(definition_words).strip()
        
        entry = {
            "word": potential_word,
            "pronunciation": pronunciation,
            "part_of_speech": pos,
            "definition": definition,
            "translation": translation,
            "unit": current_unit,
            "page": current_page,
            "correct_count": 0,
            "wrong_count": 0
        }
        
        # Dodaj wpis TYLKO jeśli ma słowo angielskie + (wymowa LUB POS LUB definicja)
        # Polskie słowa bez informacji - SKIP
        if entry["word"] and len(entry["word"]) >= 2:
            # Skip jeśli to polskie słowo bez wymowy/POS/definicji
            if re.search(r'[ąćęłńóśźż]', entry["word"]) and not entry["pronunciation"] and not entry["part_of_speech"]:
                continue
            entries.append(entry)
    
    return entries


def main():
    pdf_dir, json_dir = get_data_dirs()
    
    if not os.path.exists(pdf_dir):
        print(f"ERROR: Folder {pdf_dir} not found!")
        return
    
    os.makedirs(json_dir, exist_ok=True)
    
    pdf_files = sorted(glob.glob(os.path.join(pdf_dir, "*.pdf")))
    
    if not pdf_files:
        print(f"ERROR: No PDF files!")
        return
    
    print("\n" + "="*70)
    print("ENGLISH FILE PARSER - v3.5 OSTATECZNA PROSTA")
    print("="*70 + "\n")
    
    for pdf_path in pdf_files:
        pdf_name = os.path.basename(pdf_path)
        print(f"PDF: {pdf_name}")
        
        text = extract_text(pdf_path)
        entries = parse_vocabulary_list(text)
        
        if entries:
            output_filename = f"{os.path.splitext(pdf_name)[0]}_parsed.json"
            output_path = os.path.join(json_dir, output_filename)
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(entries, f, ensure_ascii=False, indent=2)
            
            print(f"   OK: {len(entries)} words saved\n")
        else:
            print(f"   ERROR: No data\n")
    
    print("="*70)
    print("Done!")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
