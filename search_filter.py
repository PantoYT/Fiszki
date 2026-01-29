"""
Fiszki Search & Filter
Wyszukiwanie i filtrowanie słów
"""


class SearchFilter:
    """Zarządza wyszukiwaniem i filtrowaniem słów."""
    
    @staticmethod
    def search(words, query):
        """
        Szuka słów po frazie (word, translation, definition).
        Case-insensitive.
        """
        query_lower = query.lower()
        results = []
        
        for word in words:
            if (query_lower in word.get('word', '').lower() or
                query_lower in word.get('translation', '').lower() or
                query_lower in word.get('definition', '').lower()):
                results.append(word)
        
        return results
    
    @staticmethod
    def filter_by_difficulty(words, min_error_rate=0.4):
        """
        Filtruje słowa po poziomie trudności.
        Zwraca słowa z error_rate >= min_error_rate (domyślnie >40% błędów).
        """
        difficult = []
        
        for word in words:
            correct = word.get('correct_count', 0)
            wrong = word.get('wrong_count', 0)
            total = correct + wrong
            
            if total > 0:
                error_rate = wrong / total
                if error_rate >= min_error_rate:
                    difficult.append({
                        **word,
                        'error_rate': error_rate,
                        'accuracy': (correct / total) * 100
                    })
        
        # Sort by error_rate descending (najtrudniejsze pierwsze)
        return sorted(difficult, key=lambda x: x['error_rate'], reverse=True)
    
    @staticmethod
    def filter_by_unit(words, unit):
        """Filtruje słowa po jednostce/rozdziale."""
        return [w for w in words if w.get('unit') == unit]
    
    @staticmethod
    def filter_by_status(words, status='untouched'):
        """
        Filtruje po statusie nauki:
        - 'untouched': 0 prób (correct_count=0 i wrong_count=0)
        - 'learning': 1-5 prób
        - 'known': correct_count > 3
        - 'difficult': wrong_count > correct_count
        """
        filtered = []
        
        for word in words:
            correct = word.get('correct_count', 0)
            wrong = word.get('wrong_count', 0)
            total = correct + wrong
            
            if status == 'untouched' and total == 0:
                filtered.append(word)
            elif status == 'learning' and 0 < total <= 5:
                filtered.append(word)
            elif status == 'known' and correct > 3:
                filtered.append(word)
            elif status == 'difficult' and wrong > correct and total > 0:
                filtered.append(word)
        
        return filtered
    
    @staticmethod
    def get_quick_preview(word):
        """Zwraca szybki podgląd słowa dla wyszukiwania."""
        parts = []
        if word.get('word'):
            parts.append(word['word'])
        if word.get('pronunciation'):
            parts.append(f"[{word['pronunciation']}]")
        if word.get('part_of_speech'):
            parts.append(f"({word['part_of_speech']})")
        if word.get('definition'):
            parts.append(word['definition'][:50])  # Pierwsze 50 znaków
        
        return ' '.join(parts)
    
    @staticmethod
    def get_statistics(words):
        """Zwraca statystyki dla grupy słów."""
        if not words:
            return {
                'total': 0,
                'accuracy': 0,
                'untouched': 0,
                'difficult': 0,
            }
        
        total = len(words)
        total_correct = sum(w.get('correct_count', 0) for w in words)
        total_wrong = sum(w.get('wrong_count', 0) for w in words)
        total_attempts = total_correct + total_wrong
        
        untouched = len([w for w in words if w.get('correct_count', 0) + w.get('wrong_count', 0) == 0])
        difficult = len([w for w in words if w.get('wrong_count', 0) > w.get('correct_count', 0)])
        
        accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        
        return {
            'total': total,
            'accuracy': accuracy,
            'untouched': untouched,
            'difficult': difficult,
            'attempts': total_attempts,
        }
