"""
Fiszki Decks Manager
Zarządza zdatkami (Difficult Words, Daily Review, itp)
"""


class DecksManager:
    """Zarządza specjalnymi dekkami."""
    
    @staticmethod
    def create_difficult_deck(words):
        """
        Tworzy deck z trudnymi słowami (error_rate > 50%).
        """
        difficult = []
        
        for word in words:
            correct = word.get('correct_count', 0)
            wrong = word.get('wrong_count', 0)
            total = correct + wrong
            
            if total > 0:
                error_rate = wrong / total
                if error_rate > 0.5:  # > 50% błędów
                    difficult.append({
                        **word,
                        'error_rate': error_rate,
                        'accuracy': (correct / total) * 100
                    })
        
        # Sort by error_rate descending (najtrudniejsze pierwsze)
        return sorted(difficult, key=lambda x: x['error_rate'], reverse=True)
    
    @staticmethod
    def get_deck_stats(deck):
        """Zwraca statystyki decku."""
        if not deck:
            return {
                'total': 0,
                'accuracy': 0,
            }
        
        total = len(deck)
        total_correct = sum(w.get('correct_count', 0) for w in deck)
        total_wrong = sum(w.get('wrong_count', 0) for w in deck)
        total_attempts = total_correct + total_wrong
        
        accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        avg_error_rate = sum(w.get('error_rate', 0) for w in deck) / total if total > 0 else 0
        
        return {
            'total': total,
            'accuracy': accuracy,
            'avg_error_rate': avg_error_rate,
            'attempts': total_attempts,
        }
    
    @staticmethod
    def filter_by_category(words, category):
        """
        Filtruje słowa po kategorii (POS).
        category: 'noun', 'verb', 'adjective', itp
        """
        return [w for w in words if w.get('part_of_speech', '').lower() == category.lower()]
    
    @staticmethod
    def get_categories(words):
        """Zwraca dostępne kategorie (unique POS)."""
        categories = set()
        for w in words:
            pos = w.get('part_of_speech', '')
            if pos:
                categories.add(pos)
        return sorted(list(categories))
