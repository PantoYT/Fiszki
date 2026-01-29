"""
Master Parser - Zarządca parsowania PDF-ów
Umożliwia wybór serii i uruchomienie odpowiedniego parsera.
"""

import os
import json
import subprocess
import sys


def get_project_dirs():
    """Pobiera ścieżki do głównych katalogów projektu."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if os.path.basename(script_dir) == "parsers":
        project_root = os.path.dirname(script_dir)
        parsers_dir = script_dir
    else:
        project_root = script_dir
        parsers_dir = os.path.join(script_dir, "parsers")
    
    data_dir = os.path.join(project_root, "data")
    return data_dir, parsers_dir


def check_series_availability():
    """Sprawdza dostępne serie parsowania."""
    data_dir, parsers_dir = get_project_dirs()
    
    available_series = []
    
    # Sprawdź New Enterprise
    ne_pdf_dir = os.path.join(data_dir, "new_enterprise", "pdf")
    ne_parser = os.path.join(parsers_dir, "new_enterprise_parser.py")
    if os.path.exists(ne_pdf_dir) and os.path.exists(ne_parser):
        try:
            pdf_files = [f for f in os.listdir(ne_pdf_dir) if f.endswith('.pdf')]
            if pdf_files:
                available_series.append({
                    "key": "new_enterprise",
                    "name": "New Enterprise",
                    "parser": ne_parser,
                    "pdf_dir": ne_pdf_dir,
                    "pdf_count": len(pdf_files)
                })
        except:
            pass
    
    # Sprawdź English File
    ef_pdf_dir = os.path.join(data_dir, "english_file", "pdf")
    ef_parser = os.path.join(parsers_dir, "english_file_parser.py")
    if os.path.exists(ef_pdf_dir) and os.path.exists(ef_parser):
        try:
            pdf_files = [f for f in os.listdir(ef_pdf_dir) if f.endswith('.pdf')]
            if pdf_files:
                available_series.append({
                    "key": "english_file",
                    "name": "English File",
                    "parser": ef_parser,
                    "pdf_dir": ef_pdf_dir,
                    "pdf_count": len(pdf_files)
                })
        except:
            pass
    
    return available_series


def run_parser_auto(parser_path):
    """Uruchamia parser w trybie fully automatic."""
    print(f"\n{'='*70}")
    print(f"Parser: {os.path.basename(parser_path)}")
    print(f"{'='*70}\n")
    
    result = subprocess.run(
        [sys.executable, parser_path, "--full-auto"], 
        capture_output=False, 
        text=True
    )
    
    return result.returncode == 0


def full_auto_all_series():
    """Parsuje wszystkie dostępne serie automatycznie."""
    available_series = check_series_availability()
    
    if not available_series:
        print("\n❌ Brak dostępnych serii!")
        return
    
    print("\n" + "="*70)
    print("MASTER PARSER - FULL AUTO MODE")
    print("="*70)
    print("\nDostępne serie:")
    for s in available_series:
        print(f"  • {s['name']}: {s['pdf_count']} plik(ów) PDF")
    
    confirm = input("\nCzy na pewno chcesz sparsować wszystkie serie? (t/n): ").lower()
    if confirm != 't':
        print("Anulowano.")
        return
    
    results = []
    for series in available_series:
        print(f"\n{'#'*70}")
        print(f"# {series['name'].upper()}")
        print(f"{'#'*70}")
        
        success = run_parser_auto(series['parser'])
        results.append({
            "series": series['name'],
            "success": success
        })
    
    # Podsumowanie
    print("\n" + "="*70)
    print("PODSUMOWANIE")
    print("="*70)
    for r in results:
        status = "✓ Sukces" if r['success'] else "✗ Błąd"
        print(f"{status}: {r['series']}")
    print(f"{'='*70}\n")


def main():
    """Główna funkcja Master Parsera."""
    print("\n" + "="*70)
    print("MASTER PARSER - Fiszki")
    print("="*70)
    
    available_series = check_series_availability()
    
    if not available_series:
        data_dir, parsers_dir = get_project_dirs()
        print("\n❌ Brak dostępnych serii!")
        print("\nUpewnij się, że:")
        print(f"  1. Foldery zawierają pliki PDF:")
        print(f"     • {os.path.join(data_dir, 'new_enterprise', 'pdf')}")
        print(f"     • {os.path.join(data_dir, 'english_file', 'pdf')}")
        print(f"  2. Parsery istnieją w: {parsers_dir}")
        print(f"\nAktualna struktura:")
        if os.path.exists(data_dir):
            for item in os.listdir(data_dir):
                item_path = os.path.join(data_dir, item)
                if os.path.isdir(item_path):
                    pdf_dir = os.path.join(item_path, "pdf")
                    if os.path.exists(pdf_dir):
                        pdf_count = len([f for f in os.listdir(pdf_dir) if f.endswith('.pdf')])
                        print(f"  • {item}: {pdf_count} PDF(ów)")
        return
    
    while True:
        print("\nDostępne serie:")
        for idx, s in enumerate(available_series, 1):
            print(f"{idx}. {s['name']} - {s['pdf_count']} plik(ów) PDF")
        
        print(f"\n{len(available_series) + 1}. FULL AUTO - Parsuj wszystkie automatycznie")
        print("0. Wyjście")
        
        try:
            choice = int(input("\nWybierz opcję: "))
            
            if choice == 0:
                print("Zakończono.")
                return
            
            if choice == len(available_series) + 1:
                full_auto_all_series()
                return
            
            if 1 <= choice <= len(available_series):
                series = available_series[choice - 1]
                print(f"\n▶ Uruchamianie: {series['name']}")
                print(f"  Parser: {os.path.basename(series['parser'])}")
                print(f"  Pliki PDF: {series['pdf_dir']}")
                print("\nParser uruchomi się w trybie interaktywnym...")
                input("\nNaciśnij Enter aby kontynuować...")
                
                subprocess.run([sys.executable, series['parser']])
                return
            else:
                print("❌ Nieprawidłowy wybór.")
        except ValueError:
            print("❌ Wprowadź liczbę.")
        except KeyboardInterrupt:
            print("\n\n⏹ Przerwano.")
            return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹ Przerwano przez użytkownika.")
    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        import traceback
        traceback.print_exc()