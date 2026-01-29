"""
Spaced Repetition Pro - SM-2 Algorithm (adapted for minutes)
Algorytm powtórek rozproszonego
"""

from datetime import datetime, timedelta


class SpacedRepetitionManager:
    """Zarządza powtórkami rozproszonymi na bazie SM-2."""
    
    @staticmethod
    def init_word(word):
        """Inicjalizuje słowo dla SR (SM-2)."""
        if 'sr_ease' not in word:
            word['sr_ease'] = 2.5  # Default SM-2 ease factor
            word['sr_interval'] = 1  # Minutes
            word['sr_repetitions'] = 0
            word['next_review'] = datetime.now().isoformat()
        return word
    
    @staticmethod
    def update_sr(word, quality):
        """
        Aktualizuje SR parametry na bazie odpowiedzi.
        quality: 0-5
            0 = complete blackout
            1 = incorrect, but close
            2 = incorrect
            3 = correct (difficult)
            4 = correct (but with effort)
            5 = perfect (no hesitation)
        """
        SpacedRepetitionManager.init_word(word)
        
        ease = word['sr_ease']
        interval = word['sr_interval']
        reps = word['sr_repetitions']
        
        # SM-2 formula
        new_ease = ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_ease = max(1.3, new_ease)  # Min ease
        
        if quality < 3:
            # Wrong answer
            new_reps = 0
            new_interval = 1  # Back to 1 minute
        else:
            # Correct answer
            new_reps = reps + 1
            if new_reps == 1:
                new_interval = 1  # 1 minute
            elif new_reps == 2:
                new_interval = 3  # 3 minutes
            else:
                new_interval = int(interval * new_ease)
        
        # Update word
        word['sr_ease'] = new_ease
        word['sr_interval'] = new_interval
        word['sr_repetitions'] = new_reps
        word['next_review'] = (datetime.now() + timedelta(minutes=new_interval)).isoformat()
        
        return word
    
    @staticmethod
    def get_due_words(words):
        """Zwraca słowa do powtórzenia (due now lub w przeszłości)."""
        now = datetime.now()
        due = []
        
        for word in words:
            SpacedRepetitionManager.init_word(word)
            
            next_review = datetime.fromisoformat(word['next_review'])
            if next_review <= now:
                due.append(word)
        
        return due
    
    @staticmethod
    def get_review_status(word):
        """Zwraca status powtórki słowa: 'due_now', 'today', 'later'."""
        SpacedRepetitionManager.init_word(word)
        
        now = datetime.now()
        next_review = datetime.fromisoformat(word['next_review'])
        
        diff_minutes = (next_review - now).total_seconds() / 60
        
        if diff_minutes <= 0:
            return 'due_now'
        elif diff_minutes <= 60:  # 1 hour
            return 'soon'
        elif diff_minutes <= 1440:  # 24 hours
            return 'today'
        else:
            return 'later'
    
    @staticmethod
    def get_status_emoji(status):
        """Zwraca emoji dla statusu."""
        mapping = {
            'due_now': '🔴',
            'soon': '🟠',
            'today': '🟡',
            'later': '🟢'
        }
        return mapping.get(status, '⚪')
    
    @staticmethod
    def map_correct_to_quality(is_correct):
        """Mapuje correct/wrong na quality (0-5)."""
        if is_correct:
            return 4  # "correct but with effort"
        else:
            return 2  # "incorrect"
    
    @staticmethod
    def get_stats(words):
        """Zwraca statystyki SR."""
        now = datetime.now()
        
        due_now = 0
        soon = 0
        today = 0
        later = 0
        not_started = 0
        
        for word in words:
            if word.get('sr_repetitions', 0) == 0:
                not_started += 1
            else:
                status = SpacedRepetitionManager.get_review_status(word)
                if status == 'due_now':
                    due_now += 1
                elif status == 'soon':
                    soon += 1
                elif status == 'today':
                    today += 1
                else:
                    later += 1
        
        return {
            'due_now': due_now,
            'soon': soon,
            'today': today,
            'later': later,
            'not_started': not_started,
            'total': len(words),
        }
