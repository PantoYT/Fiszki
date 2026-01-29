"""
Fiszki Export Manager
Eksportuje dane do różnych formatów
"""

import json
import os
import csv
from datetime import datetime


class ExportManager:
    """Zarządza eksportem danych do różnych formatów."""
    
    @staticmethod
    def export_to_anki(words, filename='fiszki_export.txt'):
        """
        Eksportuje słówka do formatu Anki (tab-separated).
        Format: front\tback
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for word in words:
                    front = word['word']
                    
                    # Back zawiera pronunciation, definition, translation
                    back_parts = []
                    if word.get('pronunciation'):
                        back_parts.append(f"[{word['pronunciation']}]")
                    if word.get('part_of_speech'):
                        back_parts.append(f"({word['part_of_speech']})")
                    if word.get('definition'):
                        back_parts.append(word['definition'])
                    if word.get('translation'):
                        back_parts.append(f"= {word['translation']}")
                    
                    back = ' '.join(back_parts)
                    f.write(f"{front}\t{back}\n")
            
            return True, f"Eksportowano {len(words)} słów do {filename}"
        except Exception as e:
            return False, f"Błąd eksportu: {e}"
    
    @staticmethod
    def export_to_csv(words, filename='fiszki_export.csv'):
        """Eksportuje słówka do formatu CSV."""
        try:
            if not words:
                return False, "Brak słów do eksportu"
            
            fieldnames = ['word', 'pronunciation', 'part_of_speech', 'definition', 
                         'translation', 'unit', 'page', 'correct_count', 'wrong_count']
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for word in words:
                    row = {field: word.get(field, '') for field in fieldnames}
                    writer.writerow(row)
            
            return True, f"Eksportowano {len(words)} słów do {filename}"
        except Exception as e:
            return False, f"Błąd eksportu: {e}"
    
    @staticmethod
    def export_to_json(words, filename='fiszki_export.json'):
        """Eksportuje słówka do formatu JSON."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(words, f, indent=2, ensure_ascii=False)
            
            return True, f"Eksportowano {len(words)} słów do {filename}"
        except Exception as e:
            return False, f"Błąd eksportu: {e}"
    
    @staticmethod
    def export_statistics(words, filename='fiszki_stats.txt'):
        """Eksportuje statystyki nauki."""
        try:
            total_words = len(words)
            total_correct = sum(w.get('correct_count', 0) for w in words)
            total_wrong = sum(w.get('wrong_count', 0) for w in words)
            total_attempts = total_correct + total_wrong
            
            accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
            
            stats = f"""Statystyki Fiszek
====================
Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Ogółem słów: {total_words}
Prawidłowe odpowiedzi: {total_correct}
Błędne odpowiedzi: {total_wrong}
Razem prób: {total_attempts}
Dokładność: {accuracy:.1f}%

Słowa niedokończone (0 prób): {len([w for w in words if w.get('correct_count', 0) + w.get('wrong_count', 0) == 0])}
Słowa najtrudniejsze (błędy > poprawne):
"""
            
            difficult = [(w['word'], w.get('wrong_count', 0), w.get('correct_count', 0)) 
                        for w in words if w.get('wrong_count', 0) > w.get('correct_count', 0)]
            difficult.sort(key=lambda x: x[1], reverse=True)
            
            for word, wrong, correct in difficult[:10]:
                stats += f"  - {word}: {wrong} błędy, {correct} poprawne\n"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(stats)
            
            return True, stats
        except Exception as e:
            return False, f"Błąd eksportu statystyk: {e}"
