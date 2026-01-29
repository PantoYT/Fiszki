"""
Analytics Manager
Śledzenie sesji i statystyk nauki
"""

import json
import os
from datetime import datetime, timedelta


class AnalyticsManager:
    """Zarządza historią sesji i statystykami."""
    
    ANALYTICS_FILE = '.fiszki_analytics.json'
    
    @staticmethod
    def init_analytics():
        """Inicjalizuje plik analytics."""
        if not os.path.exists(AnalyticsManager.ANALYTICS_FILE):
            AnalyticsManager.save_analytics({
                'sessions': [],
                'daily_stats': {},
            })
    
    @staticmethod
    def load_analytics():
        """Ładuje historię."""
        AnalyticsManager.init_analytics()
        try:
            with open(AnalyticsManager.ANALYTICS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'sessions': [], 'daily_stats': {}}
    
    @staticmethod
    def save_analytics(data):
        """Zapisuje historię."""
        try:
            with open(AnalyticsManager.ANALYTICS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    @staticmethod
    def record_session(session_data):
        """
        Zapisuje sesję.
        session_data: {
            'date': ISO datetime,
            'unit': 'Unit 3',
            'duration_minutes': 12,
            'words_reviewed': 15,
            'correct': 10,
            'wrong': 5,
            'accuracy': 66.7
        }
        """
        analytics = AnalyticsManager.load_analytics()
        
        session = {
            'date': session_data.get('date', datetime.now().isoformat()),
            'unit': session_data.get('unit', 'Unknown'),
            'duration_minutes': session_data.get('duration_minutes', 0),
            'words_reviewed': session_data.get('words_reviewed', 0),
            'correct': session_data.get('correct', 0),
            'wrong': session_data.get('wrong', 0),
            'accuracy': session_data.get('accuracy', 0),
        }
        
        analytics['sessions'].append(session)
        
        # Update daily stats
        day = session['date'][:10]  # YYYY-MM-DD
        if day not in analytics['daily_stats']:
            analytics['daily_stats'][day] = {
                'sessions': 0,
                'words_reviewed': 0,
                'accuracy': 0,
                'duration_minutes': 0,
            }
        
        daily = analytics['daily_stats'][day]
        daily['sessions'] += 1
        daily['words_reviewed'] += session['words_reviewed']
        daily['duration_minutes'] += session['duration_minutes']
        
        # Średnia dokładność
        if daily['sessions'] > 0:
            daily['accuracy'] = (daily['accuracy'] * (daily['sessions'] - 1) + session['accuracy']) / daily['sessions']
        
        AnalyticsManager.save_analytics(analytics)
    
    @staticmethod
    def get_last_sessions(days=7):
        """Zwraca ostatnie N dni sesji."""
        analytics = AnalyticsManager.load_analytics()
        
        now = datetime.now()
        cutoff = (now - timedelta(days=days)).date()
        
        recent = []
        for session in analytics['sessions'][-100:]:  # Sprawdź ostatnie 100
            session_date = datetime.fromisoformat(session['date']).date()
            if session_date >= cutoff:
                recent.append(session)
        
        return recent
    
    @staticmethod
    def get_7day_stats():
        """Zwraca statystyki ostatnich 7 dni."""
        analytics = AnalyticsManager.load_analytics()
        
        now = datetime.now()
        stats = {
            'total_sessions': 0,
            'total_words': 0,
            'avg_accuracy': 0,
            'total_minutes': 0,
            'daily_breakdown': {},
        }
        
        for i in range(7):
            day = (now - timedelta(days=i)).date().isoformat()
            if day in analytics['daily_stats']:
                daily = analytics['daily_stats'][day]
                stats['total_sessions'] += daily['sessions']
                stats['total_words'] += daily['words_reviewed']
                stats['total_minutes'] += daily['duration_minutes']
                if stats['total_sessions'] > 0:
                    stats['avg_accuracy'] = (stats['avg_accuracy'] * (stats['total_sessions'] - 1) + daily['accuracy']) / stats['total_sessions']
                stats['daily_breakdown'][day] = daily
        
        return stats
    
    @staticmethod
    def get_dashboard_text():
        """Zwraca tekst do wyświetlenia w dashboardzie."""
        stats = AnalyticsManager.get_7day_stats()
        sessions = AnalyticsManager.get_last_sessions(7)
        
        text = "📊 STATYSTYKI OSTATNICH 7 DNI\n"
        text += "=" * 40 + "\n\n"
        
        text += f"Sesji: {stats['total_sessions']}\n"
        text += f"Słów powtórzonych: {stats['total_words']}\n"
        text += f"Średnia dokładność: {stats['avg_accuracy']:.1f}%\n"
        text += f"Całkowity czas: {stats['total_minutes']} minut\n\n"
        
        text += "OSTATNIE SESJE:\n"
        text += "-" * 40 + "\n"
        
        for session in sessions[-10:]:  # Ostatnie 10
            date = session['date'][:10]
            time = session['date'][11:16]
            accuracy = session['accuracy']
            words = session['words_reviewed']
            text += f"{date} {time} | {words}w | {accuracy:.0f}% | {session['unit']}\n"
        
        text += "\n" + "=" * 40 + "\n"
        
        # Top performing days
        daily_breakdown = stats['daily_breakdown']
        if daily_breakdown:
            best_day = max(daily_breakdown.items(), key=lambda x: x[1]['words_reviewed'])
            text += f"\nBest day: {best_day[0]} ({best_day[1]['words_reviewed']} słów)\n"
        
        return text
    
    @staticmethod
    def get_most_studied_units():
        """Zwraca top 5 najczęściej powtarzanych jednostek."""
        analytics = AnalyticsManager.load_analytics()
        
        units = {}
        for session in analytics['sessions']:
            unit = session.get('unit', 'Unknown')
            if unit not in units:
                units[unit] = 0
            units[unit] += session['words_reviewed']
        
        sorted_units = sorted(units.items(), key=lambda x: x[1], reverse=True)
        return sorted_units[:5]
