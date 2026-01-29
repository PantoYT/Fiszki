"""
Career Paths Glossary Parser - v3.7
Parsuje słowniki Career Paths (ESP series)

Format: word [POS-UNIT] definition
Example: address book [N-COUNT-U12] An address book is an organized list...
"""

import fitz
import os
import json
import glob
import re
import sys


def get_data_dirs(category):
    """Get paths for specific Career Paths category."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    base_dir = os.path.join(project_root, "data", "career_paths", category)
    pdf_dir = os.path.join(base_dir, "pdf")
    json_dir = os.path.join(base_dir, "json")
    return pdf_dir, json_dir


def extract_text(pdf_path):
    """Extract text from PDF."""
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


def parse_career_paths_glossary(text):
    """
    Parse Career Paths glossary format:
    word [POS-UNIT] definition
    
    POS can be: N, V, ADJ, ADV, PHRA, etc
    UNIT is like U1, U2, U12 (Unit number)
    """
    
    entries = []
    current_page = 1
    
    lines = text.split('\n')
    
    for raw_line in lines:
        # Track page numbers
        page_match = re.match(r'__PAGE_(\d+)__', raw_line.strip())
        if page_match:
            current_page = int(page_match.group(1))
            continue
        
        line = raw_line.strip()
        
        if not line or len(line) < 5:
            continue
        
        # Pattern: word [POS-UNIT] definition
        # Example: address book [N-COUNT-U12] or [N−UNCOUNT−U15]
        # Supports both - and − (unicode minus)
        match = re.match(r'^(.+?)\s*\[([A-Z\-−]+)(?:[-−]U(\d+))?\]\s+(.+)$', line)
        
        if not match:
            continue
        
        word = match.group(1).strip()
        pos_unit = match.group(2).strip()  # e.g., N-COUNT
        unit_num = match.group(3) or "1"    # e.g., 12
        definition = match.group(4).strip()
        
        # Validate word (must not be pure number)
        if not word or word.isdigit() or len(word) < 2:
            continue
        
        # Extract POS (first part before any hyphen, or use full if no hyphen)
        pos_parts = pos_unit.split('-')
        pos = pos_parts[0].lower() if pos_parts else ""
        
        # Map POS codes to full names
        pos_map = {
            'N': 'n',
            'V': 'v',
            'ADJ': 'adj',
            'ADV': 'adv',
            'PHRA': 'phr',
            'PHRF': 'phr',
            'PHRV': 'phr',
        }
        
        pos = pos_map.get(pos, pos.lower())
        
        entry = {
            "word": word,
            "pronunciation": "",
            "part_of_speech": pos,
            "definition": definition,
            "translation": "",  # Career Paths don't have translations
            "unit": f"Unit {unit_num}",
            "page": current_page,
            "correct_count": 0,
            "wrong_count": 0
        }
        
        entries.append(entry)
    
    return entries


def main():
    # Get all Career Paths categories
    base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                            "data", "career_paths")
    
    if not os.path.exists(base_path):
        print(f"ERROR: {base_path} not found!")
        return
    
    categories = sorted([d for d in os.listdir(base_path) 
                        if os.path.isdir(os.path.join(base_path, d))])
    
    if not categories:
        print("ERROR: No categories found!")
        return
    
    print("\n" + "="*70)
    print("CAREER PATHS GLOSSARY PARSER - v3.7")
    print("="*70 + "\n")
    
    total_entries = 0
    
    for category in categories:
        pdf_dir, json_dir = get_data_dirs(category)
        
        if not os.path.exists(pdf_dir):
            continue
        
        os.makedirs(json_dir, exist_ok=True)
        
        pdf_files = sorted(glob.glob(os.path.join(pdf_dir, "*.pdf")))
        
        if not pdf_files:
            continue
        
        print(f"[{category}]")
        
        for pdf_path in pdf_files:
            pdf_name = os.path.basename(pdf_path)
            
            text = extract_text(pdf_path)
            entries = parse_career_paths_glossary(text)
            
            if entries:
                # Remove duplicates
                unique_entries = {}
                for entry in entries:
                    key = (entry["word"].lower(), entry["unit"])
                    if key not in unique_entries:
                        unique_entries[key] = entry
                
                final_entries = list(unique_entries.values())
                
                output_filename = f"{os.path.splitext(pdf_name)[0]}_parsed.json"
                output_path = os.path.join(json_dir, output_filename)
                
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(final_entries, f, ensure_ascii=False, indent=2)
                
                total_entries += len(final_entries)
                print(f"  {pdf_name}: {len(final_entries)} words")
        
        print()
    
    print("="*70)
    print(f"Total: {total_entries} words parsed across all categories!")
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
