"""
Fiszki Settings Manager
Zarządza preferencjami użytkownika
"""

import json
import os


class SettingsManager:
    """Zarządza ustawieniami aplikacji."""
    
    CONFIG_FILE = '.fiszki_config.json'
    
    DEFAULT_SETTINGS = {
        'dark_mode': False,
        'auto_save': True,
        'show_statistics': True,
        'keyboard_hints': True,
        'language': 'pl',  # pl, en
        'theme': 'light',  # light, dark
        'font_size': 12,
        'card_flip_animation': True,
    }
    
    def __init__(self):
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Ładuje ustawienia z pliku."""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return self.DEFAULT_SETTINGS.copy()
    
    def save_settings(self):
        """Zapisuje ustawienia do pliku."""
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Błąd przy zapisywaniu ustawień: {e}")
    
    def get(self, key, default=None):
        """Pobiera ustawienie."""
        return self.settings.get(key, default or self.DEFAULT_SETTINGS.get(key))
    
    def set(self, key, value):
        """Ustawia wartość."""
        self.settings[key] = value
        self.save_settings()
    
    def toggle(self, key):
        """Przełącza boolean setting."""
        if isinstance(self.settings.get(key), bool):
            self.set(key, not self.settings[key])
            return self.settings[key]
        return None
    
    def get_theme_colors(self):
        """Zwraca kolory dla aktualnego motywu."""
        if self.get('theme') == 'dark':
            return {
                'bg': '#1e1e1e',
                'fg': '#ffffff',
                'card_bg': '#2d2d2d',
                'button_bg': '#3d3d3d',
                'separator': '#404040',
            }
        else:
            return {
                'bg': '#ffffff',
                'fg': '#000000',
                'card_bg': '#f5f5f5',
                'button_bg': '#ffffff',
                'separator': '#cccccc',
            }
