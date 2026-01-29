"""
English File Parser
Parsuje PDF-y z serii English File i konwertuje je do formatu JSON.
"""

import fitz  # PyMuPDF
import os
import json
import glob
import re
import sys


def get_data_dirs():
    """Pobiera ścieżki do folderów PDF i JSON."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    series_dir = os.path.join(project_root, "data", "english_file")
    pdf_dir = os.path.join(series_dir, "pdf")
    json_dir = os.path.join(series_dir, "json")
    return pdf_dir, json_dir


def clean_line(line):
    """Czyści linię tekstu, usuwa linie, które nie zawierają słówek."""
    line = line.strip()
    if not line:
        return None
    skip = ["English File", "© OXFORD UNIVERSITY PRESS", "Vocabulary Banks",
            "Adverbs and adverbial phrases", "Useful words and phrases",
            "Student Book"]
    for s in skip:
        if s in line:
            return None
    return line


def parse_entry(entry_text):
    """
    Parsuje wpis ze słówkiem.
    
    Format: word [POS] /pronunciation/ definition translation
    Przykład: absent-minded adj /ˌæbsənt ˈmaɪndɪd/ She's absent-minded roztargniony
    """
    pattern = re.compile(
        r"^(?P<word>[^\s/]+?)"                  # słowo
        r"(?:\s+(?P<pos>[a-z]+))?"              # część mowy (opcjonalna)
        r"(?:\s+/(?P<pron>[^/]+)/)?"            # fonetyka (opcjonalna)
        r"\s+(?P<definition>.*)",               # definicja + tłumaczenie
        re.IGNORECASE
    )
    
    m = pattern.match(entry_text)
    if not m:
        return None
    
    data = m.groupdict()
    
    # Rozdzielenie definicji od tłumaczenia (ostatnie słowo to tłumaczenie)
    definition_text = data["definition"].strip()
    def_parts = definition_text.rsplit(" ", 1)
    
    if len(def_parts) == 2:
        definition, translation = def_parts
    else:
        definition, translation = definition_text, ""
    
    return {
        "word": data.get("word", "").strip(),
        "part_of_speech": (data.get("pos") or "").strip(),
        "pronunciation": (data.get("pron") or "").strip(),
        "definition": definition.strip(),
        "translation": translation.strip(),
        "unit": "",
        "page": 0,
        "correct_count": 0,
        "wrong_count": 0
    }


def parse_pdf(pdf_path):
    """Parsuje PDF i ekstrahuje słówka."""
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Błąd: Nie można otworzyć {pdf_path}: {e}")
        return []
    
    print(f"Parsowanie {len(doc)} stron z {os.path.basename(pdf_path)}...")
    
    entries = []
    current_unit = ""
    
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text()
        lines = [clean_line(l) for l in text.splitlines()]
        lines = [l for l in lines if l]
        
        buffer = []
        
        for line in lines:
            # Szukaj "File X" jako jednostki
            unit_match = re.search(r"File\s+(\d+[a-z]?)", line, re.IGNORECASE)
            if unit_match:
                current_unit = f"File {unit_match.group(1)}"
                continue
            
            # Dodaj linię do buffera
            buffer.append(line)
            
            # Spróbuj dopasować wpis
            entry_text = " ".join(buffer)
            entry = parse_entry(entry_text)
            
            if entry and entry["word"]:
                entry["unit"] = current_unit
                entry["page"] = page_number
                entries.append(entry)
                buffer = []
            # Jeśli nie dopasowano, czekaj na kolejną linię (definicja może być złamana)
        
        # Jeśli coś zostało w bufferze, spróbuj dopasować
        if buffer:
            entry_text = " ".join(buffer)
            entry = parse_entry(entry_text)
            if entry and entry["word"]:
                entry["unit"] = current_unit
                entry["page"] = page_number
                entries.append(entry)
    
    doc.close()
    return entries


def main():
    """Główna funkcja parsera."""
    full_auto = "--full-auto" in sys.argv
    
    pdf_dir, json_dir = get_data_dirs()
    
    if not os.path.exists(pdf_dir):
        print(f"Błąd: Folder {pdf_dir} nie istnieje!")
        return
    
    os.makedirs(json_dir, exist_ok=True)
    
    pdf_files = sorted(glob.glob(os.path.join(pdf_dir, "*.pdf")))
    
    if not pdf_files:
        print(f"Błąd: Brak plików PDF w {pdf_dir}")
        return
    
    print("\n" + "="*70)
    print("ENGLISH FILE - PARSER")
    print("="*70)
    print(f"\nZnaleziono {len(pdf_files)} plik(ów) PDF\n")
    
    for pdf_path in pdf_files:
        pdf_name = os.path.basename(pdf_path)
        entries = parse_pdf(pdf_path)
        
        output_filename = f"{os.path.splitext(pdf_name)[0]}_parsed.json"
        output_path = os.path.join(json_dir, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ {pdf_name}")
        print(f"    → {len(entries)} słówek -> {output_filename}")
    
    print(f"\n{'='*70}")
    print("Ukończono parsowanie!")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrzerwano.")
        sys.exit(1)
