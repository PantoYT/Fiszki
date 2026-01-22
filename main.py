import tkinter as tk
from tkinter import messagebox
import json
import os
import random
import re

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fiszki")
        self.root.configure(bg='white')
        
        self.words = []
        self.current_word = None
        self.is_flipped = False
        self.selected_units = []
        self.current_file = None
        self.session_active = False
        self.session_start_time = None
        self.timer_job = None
        
        self.root.minsize(900, 600)
        self.root.geometry("1000x650")
        
        self.setup_ui()
        self.root.bind('<Configure>', self.on_window_resize)
        
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
        
        self.select_btn = tk.Button(btn_row, text="Wybierz podręcznik", 
                                    command=self.select_json,
                                    font=('Arial', 10),
                                    bg='white', fg='black',
                                    relief='solid', bd=1,
                                    padx=15, pady=6,
                                    cursor='hand2')
        self.select_btn.pack(side=tk.LEFT, padx=(0, 8))
        
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
        
        self.card = tk.Label(self.card_frame, text="Wybierz podręcznik aby rozpocząć", 
                           font=('Arial', 24),
                           bg='white', fg='black',
                           wraplength=500,
                           justify=tk.CENTER)
        self.card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.flip_btn = tk.Button(self.card_container, text="Przewróć", 
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
        
        author_label = tk.Label(footer_frame, text="Wojciech Hałasa", 
                               font=('Arial', 14, 'italic'), 
                               bg='white', fg='black')
        author_label.pack(side=tk.RIGHT, padx=10)
        
    def on_window_resize(self, event):
        if self.current_word and hasattr(self, 'card_frame'):
            width = self.card_container.winfo_width()
            new_width = min(600, max(400, width - 100))
            self.card_frame.place_configure(width=new_width)
            self.card.config(wraplength=new_width - 50)
        
    def select_json(self):
        script_dir = os.path.dirname(__file__)
        data_dir = os.path.join(script_dir, "data")
        
        if not os.path.exists(data_dir):
            messagebox.showerror("Błąd", "Folder data/ nie istnieje!")
            return
            
        json_files = [f for f in os.listdir(data_dir) if f.endswith('_parsed.json')]
        
        if not json_files:
            messagebox.showwarning("Brak plików", "Nie znaleziono plików JSON")
            return
        
        select_win = tk.Toplevel(self.root)
        select_win.title("Wybierz podręcznik")
        select_win.geometry("500x400")
        select_win.configure(bg='white')
        
        container = tk.Frame(select_win, bg='white')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(container, text="Podręczniki:", 
                font=('Arial', 12, 'bold'), 
                bg='white',
                anchor='w').pack(anchor='w', pady=(0, 10))
        
        listbox = tk.Listbox(container, font=('Arial', 10), 
                            relief='solid', bd=1)
        listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        for f in json_files:
            listbox.insert(tk.END, f)
        
        def load():
            sel = listbox.curselection()
            if sel:
                file = json_files[sel[0]]
                self.load_json(os.path.join(data_dir, file))
                select_win.destroy()
        
        tk.Button(container, text="Załaduj", command=load,
                 bg='white', fg='black', font=('Arial', 10),
                 relief='solid', bd=1,
                 padx=20, pady=6,
                 cursor='hand2').pack(anchor='w')
    
    def load_json(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.words = json.load(f)
            
            self.current_file = filepath
            filename = os.path.basename(filepath)
            self.file_label.config(text=filename)
            self.show_unit_selection()
            
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można załadować:\n{e}")
    
    def natural_sort_key(self, unit):
        parts = re.findall(r'\d+|\D+', str(unit))
        return [int(part) if part.isdigit() else part for part in parts]
    
    def show_unit_selection(self):
        for widget in self.control_frame.winfo_children():
            widget.destroy()
        
        units_raw = set(w.get('unit', 'Unknown') for w in self.words)
        units = sorted(units_raw, key=self.natural_sort_key)
        

        tk.Label(self.control_frame, text="Wybierz działy:", 
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
        
        tk.Button(quick_frame, text="Żadne", 
                 command=self.select_none,
                 font=('Arial', 8),
                 bg='white', fg='black',
                 relief='solid', bd=1,
                 padx=8, pady=3,
                 cursor='hand2').pack(side=tk.LEFT, padx=(0, 4))
        
        tk.Button(quick_frame, text="Odwróć", 
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
        
        for unit in units:
            var = tk.BooleanVar(value=False)
            self.unit_vars[unit] = var
            
            count = sum(1 for w in self.words if w.get('unit') == unit)
            
            cb = tk.Checkbutton(cb_frame, 
                               text=f"Unit {unit} ({count})", 
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
            messagebox.showwarning("Uwaga", "Wybierz przynajmniej jeden dział!")
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
    
    def stop_learning(self):
        self.session_active = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        self.start_btn.config(text="Start")
        
        self.flip_btn.config(state=tk.DISABLED)
        self.correct_btn.config(state=tk.DISABLED)
        self.wrong_btn.config(state=tk.DISABLED)
        
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
            weight = max(1, 10 + (wrong * 2) - correct)
            weights.append(weight)
        
        return random.choices(available, weights=weights)[0]
    
    def show_next_card(self):
        self.current_word = self.get_next_word()
        
        if not self.current_word:
            messagebox.showinfo("Koniec", "Brak słówek!")
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
            pron = self.current_word.get('pronunciation', '')
            pos = self.current_word.get('part_of_speech', '')
            definition = self.current_word.get('definition', '')
            
            text = f"{pron}\n({pos})\n\n{definition}"
            self.card.config(text=text, font=('Arial', 16), justify=tk.LEFT)
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
        else:
            self.current_word['wrong_count'] = self.current_word.get('wrong_count', 0) + 1
            self.session_wrong += 1
        
        self.save_progress()
        self.show_next_card()
    
    def save_progress(self):
        if self.current_file and os.path.exists(self.current_file):
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    json.dump(self.words, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Błąd zapisu: {e}")
    
    def update_stats(self):
        total = len([w for w in self.words if w.get('unit') in self.selected_units])
        correct = sum(w.get('correct_count', 0) for w in self.words if w.get('unit') in self.selected_units)
        wrong = sum(w.get('wrong_count', 0) for w in self.words if w.get('unit') in self.selected_units)
        
        self.stats_label.config(text=f"Słówek w działach: {total} | Poprawne: {correct} | Błędne: {wrong}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()