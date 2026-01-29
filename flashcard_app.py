import tkinter as tk
from tkinter import messagebox
import json
import os
import random
import re
from datetime import datetime
from settings_manager import SettingsManager
from search_filter import SearchFilter
from decks_manager import DecksManager
from spaced_repetition import SpacedRepetitionManager
from analytics_manager import AnalyticsManager

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fiszki v4.0 - Vocabulary Learning")
        
        # Settings manager
        self.settings = SettingsManager()
        self.colors = self.settings.get_theme_colors()
        self.root.configure(bg=self.colors['bg'])
        
        self.words = []
        self.current_word = None
        self.is_flipped = False
        self.selected_units = []
        self.current_file = None
        self.current_series = None
        self.session_active = False
        self.session_start_time = None
        self.timer_job = None
        self.session_correct = 0
        self.session_wrong = 0
        self.quick_review_mode = False
        self.quick_review_words = []
        
        self.root.minsize(1000, 700)
        self.root.geometry("1200x750")
        
        self.setup_ui()
        self.root.bind('<Configure>', self.on_window_resize)
        self.root.bind('<space>', lambda e: self.flip_card())
        self.root.bind('<Left>', lambda e: self.answer(False))
        self.root.bind('<Right>', lambda e: self.answer(True))
        self.root.bind('<a>', lambda e: self.answer(False))
        self.root.bind('<d>', lambda e: self.answer(True))
        self.root.bind('<Control-d>', lambda e: self.toggle_dark_mode())
        self.root.bind('<Control-r>', lambda e: self.start_quick_review())
        
    def start_quick_review(self):
        """Szybka sesja - tylko znane słowa (correct > 3), auto flip."""
        if not self.words:
            messagebox.showwarning("Brak danych", "Najpierw wczytaj słowa!")
            return
        
        # Filtruj znane słowa
        known = [w for w in self.words if w.get('correct_count', 0) > 3]
        
        if not known:
            messagebox.showinfo("Quick Review", "Brak znanych słów do powtórki!\nZapraszamy do nauki.")
            return
        
        self.quick_review_mode = True
        self.quick_review_words = known
        self.session_active = True
        self.session_start_time = datetime.now()
        self.session_correct = 0
        self.session_wrong = 0
        
        stats = SearchFilter.get_statistics(known)
        messagebox.showinfo("Quick Review", 
            f"Będziesz powtarzać {stats['total']} znanych słów\n"
            f"Dokładność: {stats['accuracy']:.1f}%\n\n"
            f"Naciśnij SPACE aby zacząć")
        
        self.show_next_card_quick_review()
    
    def show_next_card_quick_review(self):
        """Pokaż następne słowo w quick review mode."""
        if not self.quick_review_words:
            self.end_session()
            return
        
        self.current_word = self.quick_review_words.pop(0)
        self.is_flipped = False
        self.card.config(text=self.current_word['word'], 
                        font=('Arial', 36, 'bold'),
                        justify=tk.CENTER)
        
        # Auto-flip po 0.5s
        self.root.after(500, self.flip_card)
        # Auto-next po 2s
        self.root.after(2000, lambda: self.answer(True))
    def toggle_dark_mode(self):
        """Przełącza dark mode i przeładowuje interfejs."""
        self.settings.toggle('dark_mode')
        self.colors = self.settings.get_theme_colors()
        self.refresh_colors()
        messagebox.showinfo("Dark Mode", 
                          f"Dark mode {'włączony' if self.settings.is_dark_mode() else 'wyłączony'}")
    
    def refresh_colors(self):
        """Aktualizuje kolory wszystkich widżetów."""
        self.root.configure(bg=self.colors['bg'])
        # Ta metoda będzie rozwinięta jeśli będzie potrzebna pełna aktualizacja UI
        
    def setup_ui(self):
        container = tk.Frame(self.root, bg='white')
        container.pack(fill=tk.BOTH, expand=True)
        
        left_panel = tk.Frame(container, bg='white', width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=30, pady=30)
        left_panel.pack_propagate(False)
        
        separator = tk.Frame(container, bg='#cccccc', width=2)
        separator.pack(side=tk.LEFT, fill=tk.Y)
        
        right_panel = tk.Frame(container, bg='white')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        title_container = tk.Frame(left_panel, bg='white')
        title_container.pack(fill=tk.X, pady=(0, 15))
        
        title = tk.Label(title_container, text="Fiszki", 
                        font=('Arial', 28, 'bold'), 
                        bg='white', fg='black')
        title.pack(anchor='center')
        
        btn_row = tk.Frame(left_panel, bg='white')
        btn_row.pack(anchor='w', pady=(0, 5))
        
        self.select_btn = tk.Button(btn_row, text="Wybierz pdręcznik", 
                                    command=self.select_series,
                                    font=('Arial', 9),
                                    bg='white', fg='black',
                                    relief='solid', bd=1,
                                    padx=10, pady=5,
                                    cursor='hand2')
        self.select_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.filter_btn = tk.Button(btn_row, text="🔍 Szukaj", 
                                    command=self.open_search_dialog,
                                    font=('Arial', 9),
                                    bg='white', fg='black',
                                    relief='solid', bd=1,
                                    padx=10, pady=5,
                                    cursor='hand2')
        self.filter_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.difficult_btn = tk.Button(btn_row, text="💪 Trudne", 
                                       command=self.start_difficult_deck,
                                       font=('Arial', 9),
                                       bg='white', fg='black',
                                       relief='solid', bd=1,
                                       padx=10, pady=5,
                                       cursor='hand2')
        self.difficult_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        btn_row2 = tk.Frame(left_panel, bg='white')
        btn_row2.pack(anchor='w', pady=(0, 5))
        
        self.category_btn = tk.Button(btn_row2, text="🏷️ Kategorie", 
                                      command=self.open_category_dialog,
                                      font=('Arial', 9),
                                      bg='white', fg='black',
                                      relief='solid', bd=1,
                                      padx=10, pady=5,
                                      cursor='hand2')
        self.category_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.dashboard_btn = tk.Button(btn_row2, text="📊 Statystyki", 
                                       command=self.show_dashboard,
                                       font=('Arial', 9),
                                       bg='white', fg='black',
                                       relief='solid', bd=1,
                                       padx=10, pady=5,
                                       cursor='hand2')
        self.dashboard_btn.pack(side=tk.LEFT)
        
        self.file_label = tk.Label(left_panel, text="", 
                                   font=('Arial', 8), 
                                   bg='white', fg='gray',
                                   anchor='w')
        self.file_label.pack(anchor='w', pady=(0, 20))
        
        select_separator = tk.Frame(left_panel, bg='#cccccc', height=2)
        select_separator.pack(fill=tk.X, pady=(0, 20))
        
        self.control_frame = tk.Frame(left_panel, bg='white')
        self.control_frame.pack(anchor='w', fill=tk.BOTH, expand=True)
        self.control_frame.pack_forget()
        
        self.card_container = tk.Frame(right_panel, bg='white')
        self.card_container.pack(fill=tk.BOTH, expand=True)
        
        timer_frame = tk.Frame(self.card_container, bg='white', 
                              relief='solid', bd=2)
        timer_frame.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        self.timer_label = tk.Label(timer_frame, text="00:00", 
                                    font=('Times New Roman', 48, 'bold'),
                                    bg='white', fg='black',
                                    padx=20, pady=10)
        self.timer_label.pack()
        
        self.start_btn = tk.Button(self.card_container, text="Start", 
                                   command=self.toggle_session,
                                   bg='black', fg='white', 
                                   font=('Arial', 12, 'bold'),
                                   relief='flat',
                                   padx=50, pady=12,
                                   cursor='hand2',
                                   state=tk.NORMAL)
        self.start_btn.place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        
        self.card_frame = tk.Frame(self.card_container, bg='white',
                                   relief='solid', bd=2)
        self.card_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=550, height=250)
        
        self.card = tk.Label(self.card_frame, text="Wybierz podrecznik aby rozpoczac", 
                           font=('Arial', 24),
                           bg='white', fg='black',
                           wraplength=500,
                           justify=tk.CENTER)
        self.card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.flip_btn = tk.Button(self.card_container, text="Przewroc", 
                                 command=self.flip_card,
                                 font=('Arial', 11),
                                 bg='white', fg='black',
                                 relief='solid', bd=1,
                                 padx=30, pady=8,
                                 state=tk.DISABLED,
                                 cursor='hand2')
        self.flip_btn.place(relx=0.5, rely=0.72, anchor=tk.CENTER)
        
        btn_frame = tk.Frame(self.card_container, bg='white')
        btn_frame.place(relx=0.5, rely=0.82, anchor=tk.CENTER)
        
        self.correct_btn = tk.Button(btn_frame, text="Znam", 
                                     command=lambda: self.answer(True),
                                     font=('Arial', 11),
                                     bg='white', fg='black',
                                     relief='solid', bd=1,
                                     padx=25, pady=8,
                                     state=tk.DISABLED,
                                     cursor='hand2')
        self.correct_btn.pack(side=tk.LEFT, padx=5)
        
        self.wrong_btn = tk.Button(btn_frame, text="Nie znam", 
                                   command=lambda: self.answer(False),
                                   font=('Arial', 11),
                                   bg='white', fg='black',
                                   relief='solid', bd=1,
                                   padx=25, pady=8,
                                   state=tk.DISABLED,
                                   cursor='hand2')
        self.wrong_btn.pack(side=tk.LEFT, padx=5)
        
        self.stats_label = tk.Label(self.card_container, text="", 
                                   font=('Arial', 9), 
                                   bg='white', fg='gray')
        self.stats_label.place(relx=0.5, rely=0.92, anchor=tk.CENTER)
        
        footer_separator = tk.Frame(right_panel, bg='#cccccc', height=2)
        footer_separator.pack(side=tk.BOTTOM, fill=tk.X, padx=0)
        
        footer_frame = tk.Frame(right_panel, bg='white')
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=(5, 10))
        
        # Informacje o skrótach
        shortcuts_label = tk.Label(footer_frame, 
                                   text="SPACE: flip | LEFT/RIGHT: no/yes | Ctrl+S: save", 
                                   font=('Arial', 8), 
                                   bg='white', fg='gray')
        shortcuts_label.pack(side=tk.LEFT, padx=10)
        
        author_label = tk.Label(footer_frame, text="Fiszki v4.0 | Wojciech Halasa", 
                               font=('Arial', 10, 'italic'), 
                               bg='white', fg='black')
        author_label.pack(side=tk.RIGHT, padx=10)
        
    def on_window_resize(self, event):
        if self.current_word and hasattr(self, 'card_frame'):
            width = self.card_container.winfo_width()
            new_width = min(600, max(400, width - 100))
            self.card_frame.place_configure(width=new_width)
            self.card.config(wraplength=new_width - 50)
    
    def select_series(self):
        script_dir = os.path.dirname(__file__)
        data_dir = os.path.join(script_dir, "data")
        
        if not os.path.exists(data_dir):
            messagebox.showerror("Blad", "Folder data/ nie istnieje!")
            return
        
        series = []
        for item in os.listdir(data_dir):
            if item.startswith('.'):
                continue
            item_path = os.path.join(data_dir, item)
            if os.path.isdir(item_path):
                # For Career Paths, check if it has categories with json files
                if item == "career_paths":
                    has_json = False
                    for category in os.listdir(item_path):
                        category_path = os.path.join(item_path, category)
                        if os.path.isdir(category_path):
                            json_dir = os.path.join(category_path, "json")
                            if os.path.exists(json_dir) and os.listdir(json_dir):
                                has_json = True
                                break
                    if has_json:
                        series.append(item)
                else:
                    # For other series, check direct json folder
                    json_dir = os.path.join(item_path, "json")
                    if os.path.exists(json_dir):
                        json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
                        if json_files:
                            series.append(item)
        
        if not series:
            messagebox.showwarning("Brak serii", "Nie znaleziono żadnych serii podręczników")
            return
        
        select_win = tk.Toplevel(self.root)
        select_win.title("Wybierz serię")
        select_win.geometry("500x400")
        select_win.configure(bg='white')
        
        container = tk.Frame(select_win, bg='white')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(container, text="Serie podręczników:", 
                font=('Arial', 12, 'bold'), 
                bg='white',
                anchor='w').pack(anchor='w', pady=(0, 10))
        
        listbox = tk.Listbox(container, font=('Arial', 10), 
                            relief='solid', bd=1)
        listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        series_display = {
            "new_enterprise": "New Enterprise",
            "english_file": "English File",
            "career_paths": "Career Paths"
        }
        
        for s in series:
            display_name = series_display.get(s, s.replace('_', ' ').title())
            listbox.insert(tk.END, display_name)
        
        def load():
            sel = listbox.curselection()
            if sel:
                series_key = series[sel[0]]
                self.select_file_from_series(series_key)
                select_win.destroy()
        
        # Bind double-click and Enter to load
        listbox.bind('<Double-Button-1>', lambda e: load())
        listbox.bind('<Return>', lambda e: load())
        
        tk.Button(container, text="Wybierz", command=load,
                 bg='white', fg='black', font=('Arial', 10),
                 relief='solid', bd=1,
                 padx=20, pady=6,
                 cursor='hand2').pack(anchor='w')
    
    def select_file_from_series(self, series_key):
        script_dir = os.path.dirname(__file__)
        data_dir = os.path.join(script_dir, "data")
        
        # Special handling for Career Paths (different directory structure)
        if series_key == "career_paths":
            self.select_career_paths_category()
            return
        
        json_dir = os.path.join(data_dir, series_key, "json")
        
        json_files = sorted([f for f in os.listdir(json_dir) if f.endswith('.json')])
        
        if not json_files:
            messagebox.showwarning("Brak plikow", f"Brak plikow JSON dla serii {series_key}")
            return
        
        select_win = tk.Toplevel(self.root)
        select_win.title("Wybierz poziom")
        select_win.geometry("500x500")
        select_win.configure(bg='white')
        
        container = tk.Frame(select_win, bg='white')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(container, text="Dostepne poziomy:", 
                font=('Arial', 12, 'bold'), 
                bg='white',
                anchor='w').pack(anchor='w', pady=(0, 10))
        
        listbox = tk.Listbox(container, font=('Arial', 10), 
                            relief='solid', bd=1)
        listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        for f in json_files:
            listbox.insert(tk.END, f.replace('_parsed.json', ''))
        
        def load():
            sel = listbox.curselection()
            if sel:
                file = json_files[sel[0]]
                self.load_json(os.path.join(json_dir, file), series_key)
                select_win.destroy()
        
        tk.Button(container, text="Zaladuj", command=load,
                 bg='white', fg='black', font=('Arial', 10),
                 relief='solid', bd=1,
                 padx=20, pady=6,
                 cursor='hand2').pack(anchor='w')
    
    def select_career_paths_category(self):
        """Special handler for Career Paths categories."""
        script_dir = os.path.dirname(__file__)
        data_dir = os.path.join(script_dir, "data", "career_paths")
        
        # List all categories (skip .template)
        categories = []
        for item in os.listdir(data_dir):
            if item.startswith('.'):  # Skip hidden folders like .template
                continue
            item_path = os.path.join(data_dir, item)
            if os.path.isdir(item_path):
                json_dir = os.path.join(item_path, "json")
                if os.path.exists(json_dir):
                    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
                    if json_files:
                        categories.append((item, json_files))
        
        if not categories:
            messagebox.showwarning("Brak kategorii", "Brak dostepnych kategorii Career Paths")
            return
        
        select_win = tk.Toplevel(self.root)
        select_win.title("Wybierz kategorie Career Paths")
        select_win.geometry("500x500")
        select_win.configure(bg='white')
        
        container = tk.Frame(select_win, bg='white')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(container, text="Dostepne kategorie:", 
                font=('Arial', 12, 'bold'), 
                bg='white',
                anchor='w').pack(anchor='w', pady=(0, 10))
        
        # Listbox z scrollbarem
        listbox_frame = tk.Frame(container, bg='white')
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(listbox_frame, font=('Arial', 10), 
                            relief='solid', bd=1,
                            yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        # Sortuj kategorie alfabetycznie
        categories.sort(key=lambda x: x[0])
        
        for cat, files in categories:
            listbox.insert(tk.END, f"{cat} ({len(files)} pliki)")
        
        def load(event=None):
            sel = listbox.curselection()
            if sel:
                category_name, json_files = categories[sel[0]]
                json_dir = os.path.join(data_dir, category_name, "json")
                
                # If only one file, load it directly
                if len(json_files) == 1:
                    self.load_json(os.path.join(json_dir, json_files[0]), "career_paths")
                    select_win.destroy()
                else:
                    # If multiple files, show another selection window
                    self.select_career_paths_file(category_name, json_files, json_dir)
                    select_win.destroy()
        
        # Bind double-click and Enter key to load
        listbox.bind('<Double-Button-1>', load)
        listbox.bind('<Return>', load)
        
        tk.Button(container, text="Zaladuj", command=load,
                 bg='white', fg='black', font=('Arial', 10),
                 relief='solid', bd=1,
                 padx=20, pady=6,
                 cursor='hand2').pack(anchor='w')
    
    def select_career_paths_file(self, category_name, json_files, json_dir):
        """Select specific JSON file within a Career Paths category."""
        select_win = tk.Toplevel(self.root)
        select_win.title(f"Wybierz plik - {category_name}")
        select_win.geometry("500x500")
        select_win.configure(bg='white')
        
        container = tk.Frame(select_win, bg='white')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(container, text=f"Pliki w kategorii {category_name}:", 
                font=('Arial', 12, 'bold'), 
                bg='white',
                anchor='w').pack(anchor='w', pady=(0, 10))
        
        listbox = tk.Listbox(container, font=('Arial', 10), 
                            relief='solid', bd=1)
        listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        for f in sorted(json_files):
            listbox.insert(tk.END, f.replace('_parsed.json', ''))
        
        def load():
            sel = listbox.curselection()
            if sel:
                file = sorted(json_files)[sel[0]]
                self.load_json(os.path.join(json_dir, file), "career_paths")
                select_win.destroy()
        
        tk.Button(container, text="Zaladuj", command=load,
                 bg='white', fg='black', font=('Arial', 10),
                 relief='solid', bd=1,
                 padx=20, pady=6,
                 cursor='hand2').pack(anchor='w')
    
    def load_json(self, filepath, series_key):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.words = json.load(f)
            
            self.current_file = filepath
            self.current_series = series_key
            filename = os.path.basename(filepath).replace('_parsed.json', '')
            self.file_label.config(text=filename)
            self.show_unit_selection()
            
        except Exception as e:
            messagebox.showerror("Blad", f"Nie mozna zaladowac:\n{e}")
    
    def natural_sort_key(self, unit):
        parts = re.findall(r'\d+|\D+', str(unit))
        return [int(part) if part.isdigit() else part for part in parts]
    
    def show_unit_selection(self):
        for widget in self.control_frame.winfo_children():
            widget.destroy()
        
        units_raw = set(w.get('unit', 'Unknown') for w in self.words)
        units = sorted(units_raw, key=self.natural_sort_key)
        
        tk.Label(self.control_frame, text="Wybierz dzialy:", 
                font=('Arial', 11, 'bold'), 
                bg='white',
                anchor='w').pack(anchor='w', pady=(0, 8))
        
        quick_frame = tk.Frame(self.control_frame, bg='white')
        quick_frame.pack(anchor='w', fill=tk.X, pady=(0, 8))
        
        tk.Button(quick_frame, text="Wszystkie", 
                 command=self.select_all,
                 font=('Arial', 8),
                 bg='white', fg='black',
                 relief='solid', bd=1,
                 padx=8, pady=3,
                 cursor='hand2').pack(side=tk.LEFT, padx=(0, 4))
        
        tk.Button(quick_frame, text="Zadne", 
                 command=self.select_none,
                 font=('Arial', 8),
                 bg='white', fg='black',
                 relief='solid', bd=1,
                 padx=8, pady=3,
                 cursor='hand2').pack(side=tk.LEFT, padx=(0, 4))
        
        tk.Button(quick_frame, text="Odwroc", 
                 command=self.invert_selection,
                 font=('Arial', 8),
                 bg='white', fg='black',
                 relief='solid', bd=1,
                 padx=8, pady=3,
                 cursor='hand2').pack(side=tk.LEFT)
        
        canvas_frame = tk.Frame(self.control_frame, bg='white', 
                               relief='solid', bd=1)
        canvas_frame.pack(anchor='w', fill=tk.BOTH, expand=True, pady=(0, 12))
        
        canvas = tk.Canvas(canvas_frame, bg='white', 
                          highlightthickness=0,
                          bd=0)
        
        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, 
                                  command=canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, 
                                  command=canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        canvas.configure(yscrollcommand=v_scrollbar.set,
                        xscrollcommand=h_scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        cb_frame = tk.Frame(canvas, bg='white')
        canvas.create_window((0, 0), window=cb_frame, anchor='nw')
        
        self.unit_vars = {}
        
        row = 0
        
        unit_label = "Unit"
        
        for unit in units:
            var = tk.BooleanVar(value=False)
            self.unit_vars[unit] = var
            
            count = sum(1 for w in self.words if w.get('unit') == unit)
            
            cb = tk.Checkbutton(cb_frame, 
                               text=f"{unit_label} {unit} ({count})", 
                               variable=var,
                               font=('Arial', 9),
                               bg='white',
                               activebackground='white',
                               anchor='w')
            cb.grid(row=row, column=0, sticky='w', padx=6, pady=1)
            row += 1
        
        cb_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        cb_frame.bind("<Configure>", on_frame_configure)
        
        self.control_frame.pack(anchor='w', fill=tk.BOTH, expand=True)
    
    def select_all(self):
        for var in self.unit_vars.values():
            var.set(True)
    
    def select_none(self):
        for var in self.unit_vars.values():
            var.set(False)
    
    def invert_selection(self):
        for var in self.unit_vars.values():
            var.set(not var.get())
    
    def toggle_session(self):
        if not self.session_active:
            self.start_learning()
        else:
            self.stop_learning()
    
    def start_learning(self):
        self.selected_units = [u for u, v in self.unit_vars.items() if v.get()]
        
        if not self.selected_units:
            messagebox.showwarning("Uwaga", "Wybierz przynajmniej jeden dzial!")
            return
        
        self.session_active = True
        self.session_start_time = tk.IntVar(value=0)
        self.session_correct = 0
        self.session_wrong = 0
        self.start_btn.config(text="Stop")
        
        self.flip_btn.config(state=tk.NORMAL)
        self.correct_btn.config(state=tk.NORMAL)
        self.wrong_btn.config(state=tk.NORMAL)
        
        self.stats_label.config(text="")
        self.timer_label.config(text="00:00")
        
        self.timer_job = self.root.after(1000, self.update_timer)
        self.show_next_card()
        self.update_stats()  # Show initial stats
    
    def stop_learning(self):
        self.session_active = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        self.start_btn.config(text="Start")
        
        self.flip_btn.config(state=tk.DISABLED)
        self.correct_btn.config(state=tk.DISABLED)
        self.wrong_btn.config(state=tk.DISABLED)
        
        # Record session analytics
        if self.session_correct + self.session_wrong > 0:
            total_attempts = self.session_correct + self.session_wrong
            accuracy = (self.session_correct / total_attempts * 100)
            duration_minutes = self.session_start_time.get() // 60 if self.session_start_time.get() else 0
            
            AnalyticsManager.record_session({
                'date': datetime.now().isoformat(),
                'unit': list(self.selected_units)[0] if self.selected_units else 'Unknown',
                'duration_minutes': duration_minutes,
                'words_reviewed': total_attempts,
                'correct': self.session_correct,
                'wrong': self.session_wrong,
                'accuracy': accuracy,
            })
        
        self.update_stats()
        self.timer_label.config(text="00:00")
    
    def update_timer(self):
        if not self.session_active:
            return
        
        self.session_start_time.set(self.session_start_time.get() + 1)
        seconds = self.session_start_time.get()
        mins = seconds // 60
        secs = seconds % 60
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
        
        self.timer_job = self.root.after(1000, self.update_timer)
    
    def get_next_word(self):
        available = [w for w in self.words if w.get('unit') in self.selected_units]
        
        if not available:
            return None
        
        weights = []
        for w in available:
            wrong = w.get('wrong_count', 0)
            correct = w.get('correct_count', 0)
            total = wrong + correct
            
            # Algorytm: słowa z błędami 3x częściej, untouched co sekundę
            if total == 0:
                # Nowe słowa: bazowa waga
                weight = 1
            else:
                # Error rate: wrong / (wrong + correct)
                error_rate = wrong / total
                # Słowa z błędami pojawiają się 3x częściej
                weight = max(1, 1 + (error_rate * 3))
            
            weights.append(weight)
        
        return random.choices(available, weights=weights)[0]
    
    def show_next_card(self):
        self.current_word = self.get_next_word()
        
        if not self.current_word:
            # Sprawdź czy wszystkie słowa w unit są zrobione
            self.check_unit_completion()
            return
        
        self.is_flipped = False
        self.card.config(text=self.current_word['word'], 
                        font=('Arial', 36, 'bold'),
                        justify=tk.CENTER)
    
    def flip_card(self):
        if not self.current_word or not self.session_active:
            return
        
        self.is_flipped = not self.is_flipped
        
        if self.is_flipped:
            pronunciation = self.current_word.get('pronunciation', '')
            part_of_speech = self.current_word.get('part_of_speech', '')
            definition = self.current_word.get('definition', '')
            translation = self.current_word.get('translation', '')
            
            parts = []
            
            if pronunciation:
                parts.append(f"/{pronunciation}/")
            
            if part_of_speech:
                parts.append(f"({part_of_speech})")
            
            if definition:
                parts.append(f"\n{definition}")
            
            if translation:
                parts.append(f"→ {translation}")
            
            text = '\n'.join(parts) if parts else "Brak informacji"
            self.card.config(text=text, font=('Arial', 14), justify=tk.LEFT)
        else:
            self.card.config(text=self.current_word['word'], 
                           font=('Arial', 36, 'bold'),
                           justify=tk.CENTER)
    
    def answer(self, correct):
        if not self.current_word or not self.session_active:
            return
        
        if correct:
            self.current_word['correct_count'] = self.current_word.get('correct_count', 0) + 1
            self.session_correct += 1
            quality = 4  # Correct with effort
        else:
            self.current_word['wrong_count'] = self.current_word.get('wrong_count', 0) + 1
            self.session_wrong += 1
            quality = 2  # Incorrect
        
        # Update SR (Spaced Repetition)
        SpacedRepetitionManager.update_sr(self.current_word, quality)
        
        self.save_progress()
        self.update_stats()  # Update display in real-time
        self.show_next_card()
    
    def check_unit_completion(self):
        """Sprawdza czy wszystkie słowa w unit są przynajmniej raz zagrań."""
        unit_words = [w for w in self.words if w.get('unit') in self.selected_units]
        not_touched = [w for w in unit_words if w.get('correct_count', 0) + w.get('wrong_count', 0) == 0]
        
        if not not_touched:
            # Wszystkie słowa mają przynajmniej jedną próbę - unit complete!
            self.show_completion_popup(unit_words)
            return
        
        messagebox.showinfo("Koniec", f"Brak więcej słów. Pozostało {len(not_touched)} nowych.")
    
    def show_completion_popup(self, unit_words):
        """Celebratory popup przy completion unit'u."""
        total = len(unit_words)
        correct = sum(w.get('correct_count', 0) for w in unit_words)
        wrong = sum(w.get('wrong_count', 0) for w in unit_words)
        total_attempts = correct + wrong
        accuracy = (correct / total_attempts * 100) if total_attempts > 0 else 0
        
        elapsed = 0
        if self.session_start_time:
            elapsed = (datetime.now() - self.session_start_time).total_seconds() // 60
        
        popup = tk.Toplevel(self.root)
        popup.title("🎉 UNIT COMPLETE!")
        popup.geometry("400x300")
        popup.configure(bg='white')
        popup.resizable(False, False)
        
        container = tk.Frame(popup, bg='white')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(container, text="🎉 UNIT COMPLETE! 🎉", 
                font=('Arial', 16, 'bold'), 
                bg='white', fg='black').pack(pady=(0, 20))
        
        stats_text = f"""
Słowa: {total}/15
Poprawne: {correct}
Błędy: {wrong}
Dokładność: {accuracy:.1f}%
Czas: {elapsed} minut
"""
        
        tk.Label(container, text=stats_text, 
                font=('Arial', 11), 
                bg='white', fg='black',
                justify=tk.LEFT).pack(pady=10)
        
        tk.Label(container, text="Świetna robota! 👏", 
                font=('Arial', 12, 'italic'), 
                bg='white', fg='gray').pack(pady=(20, 0))
        
        tk.Button(container, text="OK", command=popup.destroy,
                 bg='black', fg='white', font=('Arial', 10),
                 relief='flat',
                 padx=30, pady=8,
                 cursor='hand2').pack(pady=(20, 0))
        
        self.session_active = False
    
    def start_difficult_deck(self):
        """Uruchamia sesję z trudnymi słowami (error_rate > 50%)."""
        if not self.words:
            messagebox.showwarning("Brak danych", "Najpierw wczytaj słowa!")
            return
        
        difficult_words = DecksManager.create_difficult_deck(self.words)
        
        if not difficult_words:
            messagebox.showinfo("Brak trudnych słów", "Gratulujesz! Wszystkie słowa masz dobrze!")
            return
        
        stats = DecksManager.get_deck_stats(difficult_words)
        
        self.selected_units = set(w.get('unit', 'Unknown') for w in difficult_words)
        self.words = difficult_words  # Tymczasowo ustaw words do trudnych
        
        self.session_active = True
        self.session_start_time = datetime.now()
        self.session_correct = 0
        self.session_wrong = 0
        
        messagebox.showinfo("Trudne słowa", 
            f"Sesja: {stats['total']} trudnych słów\n"
            f"Średnia dokładność: {stats['accuracy']:.1f}%\n\n"
            f"Naciśnij SPACE aby zacząć")
        
        self.show_next_card()
    
    def open_category_dialog(self):
        """Otwiera dialog do wyboru kategorii (POS: noun, verb, itp)."""
        if not self.words:
            messagebox.showwarning("Brak danych", "Najpierw wczytaj słowa!")
            return
        
        categories = DecksManager.get_categories(self.words)
        
        if not categories:
            messagebox.showinfo("Brak kategorii", "Słowa nie mają zdefiniowanych kategorii (POS)")
            return
        
        cat_window = tk.Toplevel(self.root)
        cat_window.title("🏷️ Wybierz Kategorię")
        cat_window.geometry("400x400")
        cat_window.configure(bg='white')
        
        container = tk.Frame(cat_window, bg='white')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(container, text="Kategorie:", 
                font=('Arial', 12, 'bold'), 
                bg='white',
                anchor='w').pack(anchor='w', pady=(0, 10))
        
        listbox = tk.Listbox(container, font=('Arial', 10), 
                            relief='solid', bd=1)
        listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        for cat in categories:
            count = len(DecksManager.filter_by_category(self.words, cat))
            listbox.insert(tk.END, f"{cat} ({count})")
        
        def load_category():
            sel = listbox.curselection()
            if sel:
                category = categories[sel[0]]
                cat_words = DecksManager.filter_by_category(self.words, category)
                
                self.selected_units = set(w.get('unit', 'Unknown') for w in cat_words)
                self.words = cat_words
                
                self.session_active = True
                self.session_start_time = datetime.now()
                self.session_correct = 0
                self.session_wrong = 0
                
                messagebox.showinfo("Kategoria", 
                    f"Sesja: {len(cat_words)} słów ({category})\n\n"
                    f"Naciśnij SPACE aby zacząć")
                
                self.show_next_card()
                cat_window.destroy()
        
        tk.Button(container, text="Zaladuj", command=load_category,
                 bg='white', fg='black', font=('Arial', 10),
                 relief='solid', bd=1,
                 padx=20, pady=6,
                 cursor='hand2').pack(anchor='w')
    
    def show_dashboard(self):
        """Pokazuje dashboard ze statystykami."""
        dash_window = tk.Toplevel(self.root)
        dash_window.title("📊 Statystyki Nauki")
        dash_window.geometry("700x600")
        dash_window.configure(bg='white')
        
        container = tk.Frame(dash_window, bg='white')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Dashboard text
        dashboard_text = AnalyticsManager.get_dashboard_text()
        
        text_widget = tk.Text(container, font=('Courier', 10), 
                             height=25, width=85,
                             bg='white', fg='black',
                             relief='solid', bd=1)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        text_widget.insert(tk.END, dashboard_text)
        text_widget.config(state=tk.DISABLED)
        
        # Top units
        top_units = AnalyticsManager.get_most_studied_units()
        
        units_text = "\n\n🏆 TOP JEDNOSTKI:\n"
        for unit, words in top_units:
            units_text += f"  {unit}: {words} słów\n"
        
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(tk.END, units_text)
        text_widget.config(state=tk.DISABLED)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(container, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        tk.Button(container, text="Zamknij", command=dash_window.destroy,
                 bg='white', fg='black', font=('Arial', 10),
                 relief='solid', bd=1,
                 padx=20, pady=6,
                 cursor='hand2').pack()
    
    def open_search_dialog(self):
        """Otwiera dialog do wyszukiwania i filtrowania słów."""
        if not self.words:
            messagebox.showwarning("Brak danych", "Najpierw wczytaj słowa!")
            return
        
        search_window = tk.Toplevel(self.root)
        search_window.title("🔍 Szukaj i Filtruj")
        search_window.geometry("600x500")
        search_window.resizable(False, False)
        
        # Search frame
        search_frame = tk.Frame(search_window, bg='white')
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_frame, text="Szukaj słowa:", font=('Arial', 10), bg='white').pack(anchor='w')
        search_entry = tk.Entry(search_frame, font=('Arial', 10), width=50)
        search_entry.pack(fill=tk.X, pady=(5, 10))
        search_entry.focus()
        
        # Filter buttons frame
        filter_frame = tk.Frame(search_window, bg='white')
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(filter_frame, text="Filtruj:", font=('Arial', 10), bg='white').pack(anchor='w')
        btn_frame = tk.Frame(filter_frame, bg='white')
        btn_frame.pack(anchor='w', pady=5)
        
        buttons_config = [
            ("Wszystkie", 'all'),
            ("Nowe (0 prób)", 'untouched'),
            ("Trudne (błędy)", 'difficult'),
            ("Znane (>3x OK)", 'known'),
        ]
        
        selected_filter = tk.StringVar(value='all')
        
        for label, value in buttons_config:
            tk.Radiobutton(btn_frame, text=label, variable=selected_filter, 
                          value=value, font=('Arial', 9), bg='white').pack(anchor='w')
        
        # Results frame
        tk.Label(search_window, text="Wyniki (max 50):", font=('Arial', 10), 
                bg='white').pack(anchor='w', padx=10, pady=(10, 0))
        
        results_frame = tk.Frame(search_window, bg='white', relief='solid', bd=1)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        scrollbar = tk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        results_text = tk.Text(results_frame, font=('Arial', 9), height=15, width=70,
                              yscrollcommand=scrollbar.set, bg='white', fg='black')
        results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=results_text.yview)
        
        def do_search():
            """Szukaj i filtruj."""
            results_text.delete(1.0, tk.END)
            
            query = search_entry.get().strip()
            filter_type = selected_filter.get()
            
            # Wyszukaj
            if query:
                results = SearchFilter.search(self.words, query)
            else:
                results = self.words
            
            # Filtruj
            if filter_type == 'untouched':
                results = SearchFilter.filter_by_status(results, 'untouched')
            elif filter_type == 'difficult':
                results = SearchFilter.filter_by_status(results, 'difficult')
            elif filter_type == 'known':
                results = SearchFilter.filter_by_status(results, 'known')
            
            # Pokaż wyniki
            if not results:
                results_text.insert(tk.END, "Brak wyników")
                return
            
            stats = SearchFilter.get_statistics(results)
            header = f"Znalezione: {stats['total']} | Dokładność: {stats['accuracy']:.1f}% | Nowe: {stats['untouched']} | Trudne: {stats['difficult']}\n"
            header += "=" * 65 + "\n\n"
            results_text.insert(tk.END, header)
            
            for word in results[:50]:
                preview = SearchFilter.get_quick_preview(word)
                correct = word.get('correct_count', 0)
                wrong = word.get('wrong_count', 0)
                status = f" [{correct}✓ {wrong}✗]" if correct + wrong > 0 else " [NEW]"
                results_text.insert(tk.END, f"{preview}{status}\n\n")
        
        def on_entry_change(event=None):
            """Auto-search na każdą zmianę."""
            do_search()
        
        search_entry.bind('<KeyRelease>', on_entry_change)
        selected_filter.trace('w', lambda *args: do_search())
        
        # Initial search
        do_search()
    
    def save_progress(self):
        if self.current_file and os.path.exists(self.current_file):
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    json.dump(self.words, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Blad zapisu: {e}")
    
    def update_stats(self):
        total = len([w for w in self.words if w.get('unit') in self.selected_units])
        correct = sum(w.get('correct_count', 0) for w in self.words if w.get('unit') in self.selected_units)
        wrong = sum(w.get('wrong_count', 0) for w in self.words if w.get('unit') in self.selected_units)
        
        if self.session_active:
            accuracy = ((self.session_correct / (self.session_correct + self.session_wrong)) * 100) if (self.session_correct + self.session_wrong) > 0 else 0
            text = f"Seria: {self.session_correct}/{self.session_correct + self.session_wrong} ({accuracy:.0f}%) | Total poprawne: {correct} | bledy: {wrong}"
        else:
            text = f"Slowek: {total} | Poprawne (total): {correct} | Bledne (total): {wrong}"
        
        self.stats_label.config(text=text)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()