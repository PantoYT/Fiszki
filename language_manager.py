"""
Fiszki Language Manager
Obsługa wielojęzyczna - German-Polish support
"""


class LanguageManager:
    """Zarządza obsługą języków."""
    
    SUPPORTED_LANGUAGES = {
        'pl': 'Polski',
        'de': 'Deutsch (Polski)',
    }
    
    @staticmethod
    def detect_language(words):
        """
        Detektuje język słów na bazie szerokości tradycji.
        Sprawdza czy są słowa niemieckie czy polskie w translation field.
        """
        if not words:
            return 'pl'
        
        # Heurystyka: sprawdź czy jest "Deutsch" lub "German" w nazwie
        german_indicators = 0
        polish_indicators = 0
        
        for word in words[:20]:  # Sprawdź pierwsze 20 słów
            translation = word.get('translation', '').lower()
            if any(indicator in translation for indicator in ['der ', 'die ', 'das ', 'heit', 'ung']):
                german_indicators += 1
            if any(indicator in translation for indicator in ['ość', 'anie', 'enie']):
                polish_indicators += 1
        
        return 'de' if german_indicators > polish_indicators else 'pl'
    
    @staticmethod
    def get_language_display(language_code):
        """Zwraca pełną nazwę języka."""
        return LanguageManager.SUPPORTED_LANGUAGES.get(language_code, 'English')
    
    @staticmethod
    def format_word_with_language(word, language_code):
        """Formatuje słowo z informacją o języku."""
        formatted = {
            **word,
            'language': language_code,
        }
        
        if language_code == 'de':
            # Dla niemieczyzny: pokaż artykuł (der/die/das)
            translation = word.get('translation', '')
            if translation and translation[0].isupper():
                # Spróbuj wydobyć artykuł z translation
                formatted['article'] = LanguageManager.extract_article(translation)
        
        return formatted
    
    @staticmethod
    def extract_article(german_word):
        """Wydobywa artykuł niemiecki (der, die, das) z wyrazu."""
        articles = ['der ', 'die ', 'das ']
        for article in articles:
            if german_word.lower().startswith(article):
                return article.strip()
        return ''
    
    @staticmethod
    def is_german_support_available():
        """Sprawdza czy aplikacja wspiera niemiecki."""
        return True
    
    @staticmethod
    def get_language_pack(language_code):
        """Zwraca tłumaczenie UI dla danego języka."""
        packs = {
            'pl': {
                'select_textbook': 'Wybierz podręcznik',
                'select_units': 'Wybierz działy',
                'start': 'Start',
                'flip': 'Przewróć',
                'known': 'Znam',
                'unknown': 'Nie znam',
                'search': '🔍 Szukaj',
                'difficult': '💪 Trudne',
                'categories': '🏷️ Kategorie',
                'quick_review': 'Quick Review',
                'no_data': 'Brak danych',
                'load_first': 'Najpierw wczytaj słowa!',
            },
            'de': {
                'select_textbook': 'Lehrbuch wählen',
                'select_units': 'Einheiten wählen',
                'start': 'Start',
                'flip': 'Umdrehen',
                'known': 'Weiß',
                'unknown': 'Nicht bekannt',
                'search': '🔍 Suchen',
                'difficult': '💪 Schwierig',
                'categories': '🏷️ Kategorien',
                'quick_review': 'Quick Review',
                'no_data': 'Keine Daten',
                'load_first': 'Laden Sie zunächst Wörter!',
            }
        }
        return packs.get(language_code, packs['pl'])
