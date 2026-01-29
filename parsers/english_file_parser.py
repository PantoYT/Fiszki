import fitz  # PyMuPDF
import os
import json
import glob
import re

PDF_DIR = "data/english_file/pdf"
JSON_DIR = "data/english_file/json"
os.makedirs(JSON_DIR, exist_ok=True)

# Funkcja do czyszczenia linii
def clean_line(line):
    line = line.strip()
    if not line:
        return None
    skip = ["English File", "© OXFORD UNIVERSITY PRESS", "Vocabulary Banks",
            "Adverbs and adverbial phrases", "Useful words and phrases"]
    for s in skip:
        if s in line:
            return None
    return line

# Funkcja do wyłuskania słowa + część mowy + fonetyka
def parse_entry(entry_text):
    """
    Przykładowy wpis w PDF:
    absent-minded  adj /ˌæbsənt ˈmaɪndɪd/ She’s so absent-minded – she’s always forgetting things. roztargniony
    """
    pattern = re.compile(
        r"^(?P<word>[^\s]+)"                  # słowo
        r"(?:\s+(?P<pos>[a-z]+))?"           # część mowy
        r"(?:\s+/(?P<pron>[^/]+)/)?"         # fonetyka
        r"\s+(?P<definition>.*)"             # definicja + przykład + tłumaczenie
    )
    m = pattern.match(entry_text)
    if not m:
        return None
    data = m.groupdict()
    # Rozdzielenie definicji od tłumaczenia (ostatnie słowo to tłumaczenie)
    # Przy PDF English File, tłumaczenie to zazwyczaj ostatnie słowa oddzielone spacją
    def_parts = data["definition"].rsplit(" ", 1)
    if len(def_parts) == 2:
        definition, translation = def_parts
    else:
        definition, translation = data["definition"], ""
    return {
        "word": data.get("word", ""),
        "part_of_speech": data.get("pos") or "",
        "pronunciation": data.get("pron") or "",
        "definition": definition.strip(),
        "translation": translation.strip(),
        "unit": "",
        "page": 0,
        "correct_count": 0,
        "wrong_count": 0
    }

# Główna funkcja parsera
def parse_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    entries = []
    current_unit = ""
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text()
        lines = [clean_line(l) for l in text.splitlines()]
        lines = [l for l in lines if l]
        # Scal linie w jeden strumień tekstu, rozdzielimy potem po słowach
        buffer = []
        for line in lines:
            # Jeśli znajdziemy nagłówek File X
            unit_match = re.search(r"File (\d+)", line, re.IGNORECASE)
            if unit_match:
                current_unit = f"File {unit_match.group(1)}"
                continue
            # Jeśli linia zaczyna się od słowa (mała litera lub znak)
            buffer.append(line)
            # Próba dopasowania słowa
            entry_text = " ".join(buffer)
            entry = parse_entry(entry_text)
            if entry:
                entry["unit"] = current_unit
                entry["page"] = page_number
                entries.append(entry)
                buffer = []  # wyczyść buffer po dopasowaniu
            else:
                # Czekaj na kolejną linię PDF – często definicja jest złamana
                continue
        # Jeśli coś zostało w bufferze po stronie, spróbuj dopasować na siłę
        if buffer:
            entry_text = " ".join(buffer)
            entry = parse_entry(entry_text)
            if entry:
                entry["unit"] = current_unit
                entry["page"] = page_number
                entries.append(entry)
            buffer = []

    return entries

# Przetwarzanie wszystkich PDF w folderze
pdf_files = glob.glob(os.path.join(PDF_DIR, "*.pdf"))
if not pdf_files:
    print("Brak PDF-ów w folderze:", PDF_DIR)
else:
    for pdf_path in pdf_files:
        print("Przetwarzanie:", pdf_path)
        entries = parse_pdf(pdf_path)
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        json_path = os.path.join(JSON_DIR, f"{pdf_name}_parsed.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        print(f"Zapisano {len(entries)} słówek do {json_path}")
