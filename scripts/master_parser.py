#!/usr/bin/env python3
"""
Master Parser - Unified interface for all vocabulary parsers
Manages New Enterprise, English File, and Career Paths parsing
"""

import os
import sys
import subprocess
from pathlib import Path


def get_parsers_dir():
    """Get absolute path to parsers directory"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "parsers")


def get_data_dir():
    """Get absolute path to data directory"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "data")


def check_parser_exists(parser_name):
    """Check if parser file exists"""
    parsers_dir = get_parsers_dir()
    parser_path = os.path.join(parsers_dir, f"{parser_name}_parser.py")
    return os.path.exists(parser_path)


def check_pdfs_exist(series_name):
    """Check if PDFs exist for a series"""
    data_dir = get_data_dir()
    
    if series_name == "career_paths":
        # For Career Paths, check if any category has PDFs
        cp_dir = os.path.join(data_dir, "career_paths")
        if os.path.exists(cp_dir):
            for category in os.listdir(cp_dir):
                if category.startswith('.'):
                    continue
                pdf_dir = os.path.join(cp_dir, category, "pdf")
                if os.path.exists(pdf_dir) and os.listdir(pdf_dir):
                    return True
        return False
    else:
        pdf_dir = os.path.join(data_dir, series_name, "pdf")
        if os.path.exists(pdf_dir):
            pdfs = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
            return len(pdfs) > 0
        return False


def run_parser(parser_name, full_auto=False):
    """Run a specific parser"""
    parsers_dir = get_parsers_dir()
    parser_path = os.path.join(parsers_dir, f"{parser_name}_parser.py")
    
    if not os.path.exists(parser_path):
        print(f" Parser nie znaleziony: {parser_path}")
        return False
    
    try:
        cmd = [sys.executable, parser_path]
        if full_auto:
            cmd.append("--full-auto")
        
        print(f"\n Uruchamianie {parser_name} parser...")
        result = subprocess.run(cmd, cwd=parsers_dir)
        
        return result.returncode == 0
    except Exception as e:
        print(f" Błąd przy uruchamianiu parsera: {e}")
        return False


def show_menu():
    """Display main menu"""
    print("\n" + "="*70)
    print(" MASTER PARSER - Wersja 4.0")
    print("="*70)
    print("\nWybierz co chcesz parsować:\n")
    print("1⃣  New Enterprise (seria zaawansowanych podręczników)")
    print("2⃣  English File (seria z 5 poziomami)")
    print("3⃣  Career Paths (34 kategorie zawodowe)")
    print("\n0⃣  Wyjście\n")


def check_series_status():
    """Check and display status of all series"""
    data_dir = get_data_dir()
    
    print("\n" + "="*70)
    print(" STATUS SERII")
    print("="*70 + "\n")
    
    # New Enterprise
    ne_pdf_dir = os.path.join(data_dir, "new_enterprise", "pdf")
    ne_json_dir = os.path.join(data_dir, "new_enterprise", "json")
    if os.path.exists(ne_pdf_dir):
        ne_pdfs = len([f for f in os.listdir(ne_pdf_dir) if f.endswith('.pdf')])
        ne_jsons = len([f for f in os.listdir(ne_json_dir) if f.endswith('.json')]) if os.path.exists(ne_json_dir) else 0
        print(f" New Enterprise: {ne_pdfs} PDF → {ne_jsons} JSON")
    
    # English File
    ef_pdf_dir = os.path.join(data_dir, "english_file", "pdf")
    ef_json_dir = os.path.join(data_dir, "english_file", "json")
    if os.path.exists(ef_pdf_dir):
        ef_pdfs = len([f for f in os.listdir(ef_pdf_dir) if f.endswith('.pdf')])
        ef_jsons = len([f for f in os.listdir(ef_json_dir) if f.endswith('.json')]) if os.path.exists(ef_json_dir) else 0
        print(f" English File: {ef_pdfs} PDF → {ef_jsons} JSON")
    
    # Career Paths
    cp_dir = os.path.join(data_dir, "career_paths")
    total_cp_pdfs = 0
    total_cp_jsons = 0
    cp_categories = 0
    
    if os.path.exists(cp_dir):
        for category in os.listdir(cp_dir):
            if category.startswith('.'):
                continue
            category_path = os.path.join(cp_dir, category)
            if os.path.isdir(category_path):
                cp_categories += 1
                pdf_dir = os.path.join(category_path, "pdf")
                json_dir = os.path.join(category_path, "json")
                if os.path.exists(pdf_dir):
                    total_cp_pdfs += len([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
                if os.path.exists(json_dir):
                    total_cp_jsons += len([f for f in os.listdir(json_dir) if f.endswith('.json')])
    
    print(f" Career Paths: {total_cp_pdfs} PDF ({cp_categories} kategorie) → {total_cp_jsons} JSON")
    print()


def main():
    """Main entry point"""
    while True:
        show_menu()
        check_series_status()
        
        choice = input("Twój wybór: ").strip()
        
        if choice == "0":
            print("\n Do widzenia!\n")
            break
        
        elif choice == "1":
            if not check_pdfs_exist("new_enterprise"):
                print("\n  Brak PDF-ów dla New Enterprise!")
                print("   Dodaj PDF-y do: data/new_enterprise/pdf/\n")
                input("Wciśnij ENTER aby kontynuować...")
                continue
            
            print("\n Opcje parsowania New Enterprise:")
            print("1. Ręcznie - przeglądaj każdy wpis")
            print("2. Szybko - auto-accept wszystkie")
            print("3. Wróć\n")
            
            sub_choice = input("Wybór: ").strip()
            
            if sub_choice == "1":
                run_parser("new_enterprise", full_auto=False)
            elif sub_choice == "2":
                run_parser("new_enterprise", full_auto=True)
            
            input("\nWciśnij ENTER aby kontynuować...")
        
        elif choice == "2":
            if not check_pdfs_exist("english_file"):
                print("\n  Brak PDF-ów dla English File!")
                print("   Dodaj PDF-y do: data/english_file/pdf/\n")
                input("Wciśnij ENTER aby kontynuować...")
                continue
            
            print("\n Opcje parsowania English File:")
            print("1. Ręcznie - przeglądaj każdy wpis")
            print("2. Szybko - auto-accept wszystkie")
            print("3. Wróć\n")
            
            sub_choice = input("Wybór: ").strip()
            
            if sub_choice == "1":
                run_parser("english_file", full_auto=False)
            elif sub_choice == "2":
                run_parser("english_file", full_auto=True)
            
            input("\nWciśnij ENTER aby kontynuować...")
        
        elif choice == "3":
            if not check_pdfs_exist("career_paths"):
                print("\n  Brak PDF-ów dla Career Paths!")
                print("   Dodaj PDF-y do: data/career_paths/[kategoria]/pdf/\n")
                input("Wciśnij ENTER aby kontynuować...")
                continue
            
            print("\n Opcje parsowania Career Paths:")
            print("1. Ręcznie - przeglądaj każdy wpis")
            print("2. Szybko - auto-accept wszystkie (WSZYSTKIE 34 KATEGORIE)")
            print("3. Wróć\n")
            
            sub_choice = input("Wybór: ").strip()
            
            if sub_choice == "1":
                run_parser("career_paths", full_auto=False)
            elif sub_choice == "2":
                print("\n⏳ Parsowanie wszystkich 34 kategorii Career Paths...")
                print("   (To może potrwać chwilę)\n")
                run_parser("career_paths", full_auto=True)
            
            input("\nWciśnij ENTER aby kontynuować...")
        
        else:
            print("\n Nieznany wybór! Spróbuj jeszcze raz.\n")
            input("Wciśnij ENTER aby kontynuować...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Przerwane przez użytkownika\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n Błąd krytyczny: {e}\n")
        sys.exit(1)
