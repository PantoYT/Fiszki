"""
Base Parser - wspólny kod dla wszystkich parserów
"""

import json
import os
import re
from pathlib import Path


class BaseVocabularyParser:
    """Base class dla wszystkich vocabulary parserów"""
    
    # Override w subclassach
    SERIES_NAME = "unknown"
    DATA_FOLDER = "data"
    
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(self.script_dir)
        self.series_dir = os.path.join(self.project_root, self.DATA_FOLDER, self.SERIES_NAME)
        self.pdf_dir = os.path.join(self.series_dir, "pdf")
        self.json_dir = os.path.join(self.series_dir, "json")
    
    def ensure_directories(self):
        """Stwórz directories jeśli nie istnieją"""
        os.makedirs(self.json_dir, exist_ok=True)
    
    def save_json(self, data, filename):
        """Zapisz dane do JSON z UTF-8"""
        try:
            filepath = os.path.join(self.json_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"ERROR saving {filename}: {e}")
            return False
    
    def load_json(self, filepath):
        """Załaduj JSON z UTF-8"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"ERROR loading {filepath}: {e}")
            return None
    
    def normalize_word(self, word):
        """Znormalizuj słowo"""
        return word.strip().lower()
    
    def deduplicate(self, entries, key_func):
        """Usuń duplikaty na podstawie key_func"""
        seen = {}
        unique = []
        
        for entry in entries:
            key = key_func(entry)
            if key not in seen:
                seen[key] = True
                unique.append(entry)
        
        return unique
    
    def create_entry(self, word, unit="", **kwargs):
        """Stwórz entry słownika"""
        entry = {
            "word": word.strip(),
            "unit": str(unit).strip(),
        }
        
        # Opcjonalne pola
        for field in ['pronunciation', 'part_of_speech', 'definition', 'translation']:
            if field in kwargs and kwargs[field]:
                entry[field] = str(kwargs[field]).strip()
        
        # Spaced repetition fields (domyślnie)
        entry.update({
            'error_rate': 0.0,
            'correct_count': 0,
            'wrong_count': 0,
            'sr_interval': 1,
            'sr_repetitions': 0,
            'sr_ease': 2.5,
        })
        
        return entry


class SimpleVocabularyParser(BaseVocabularyParser):
    """Parser dla simple format: word | pronunciation | POS | definition"""
    
    def parse_line(self, line):
        """Parsuj pojedynczą linię"""
        parts = line.split('|')
        if len(parts) < 1:
            return None
        
        entry = self.create_entry(parts[0].strip())
        
        if len(parts) > 1:
            entry['pronunciation'] = parts[1].strip()
        if len(parts) > 2:
            entry['part_of_speech'] = parts[2].strip()
        if len(parts) > 3:
            entry['definition'] = parts[3].strip()
        
        return entry


class PDFVocabularyParser(BaseVocabularyParser):
    """Base dla parserów z PDF"""
    
    def extract_text_from_pdf(self, pdf_path):
        """Ekstrahuj text z PDF"""
        try:
            import fitz
            doc = fitz.open(pdf_path)
            text = ""
            for page_num, page in enumerate(doc):
                text += f"__PAGE_{page_num+1}__\n"
                text += page.get_text() + "\n"
            doc.close()
            return text
        except ImportError:
            print("ERROR: PyMuPDF not installed. pip install PyMuPDF")
            return ""
        except Exception as e:
            print(f"ERROR extracting text from {pdf_path}: {e}")
            return ""
    
    def get_pdf_files(self):
        """Pobierz wszystkie PDF files"""
        if not os.path.exists(self.pdf_dir):
            return []
        return sorted([f for f in os.listdir(self.pdf_dir) if f.endswith('.pdf')])


if __name__ == "__main__":
    print("Base parser loaded successfully")
