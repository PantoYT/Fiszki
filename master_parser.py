import os
import json
import subprocess
import sys

def get_project_dirs():
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
    data_dir, parsers_dir = get_project_dirs()
    
    available_series = []
    
    ne_pdf_dir = os.path.join(data_dir, "new_enterprise", "pdf")
    ne_parser = os.path.join(parsers_dir, "new_enterprise_parser.py")
    if os.path.exists(ne_pdf_dir) and os.path.exists(ne_parser):
        pdf_files = [f for f in os.listdir(ne_pdf_dir) if f.endswith('.pdf')]
        if pdf_files:
            available_series.append({
                "key": "new_enterprise",
                "name": "New Enterprise",
                "parser": ne_parser,
                "pdf_dir": ne_pdf_dir,
                "pdf_count": len(pdf_files)
            })
    
    ef_pdf_dir = os.path.join(data_dir, "english_file", "pdf")
    ef_parser = os.path.join(parsers_dir, "english_file_parser.py")
    if os.path.exists(ef_pdf_dir) and os.path.exists(ef_parser):
        pdf_files = [f for f in os.listdir(ef_pdf_dir) if f.endswith('.pdf')]
        if pdf_files:
            available_series.append({
                "key": "english_file",
                "name": "English File",
                "parser": ef_parser,
                "pdf_dir": ef_pdf_dir,
                "pdf_count": len(pdf_files)
            })
    
    return available_series

def run_parser_auto(parser_path):
    print(f"\n{'='*60}")
    print(f"Uruchamianie: {os.path.basename(parser_path)}")
    print(f"{'='*60}\n")
    
    result = subprocess.run([sys.executable, parser_path, "--full-auto"], 
                          capture_output=False, 
                          text=True)
    
    return result.returncode == 0

def full_auto_all_series():
    available_series = check_series_availability()
    
    if not available_series:
        print("Brak dostepnych serii z plikami PDF i parserami!")
        return
    
    print("\n" + "="*60)
    print("FULL AUTO - Parsowanie wszystkich serii")
    print("="*60)
    print("\nDostepne serie:")
    for s in available_series:
        print(f"  {s['name']}: {s['pdf_count']} plikow PDF")
    
    confirm = input("\nCzy na pewno chcesz sparsowac wszystkie serie? (t/n): ").lower()
    if confirm != 't':
        print("Anulowano.")
        return
    
    results = []
    for series in available_series:
        print(f"\n\n{'#'*60}")
        print(f"# Parsowanie: {series['name']}")
        print(f"{'#'*60}\n")
        
        success = run_parser_auto(series['parser'])
        results.append({
            "series": series['name'],
            "success": success
        })
    
    print("\n\n" + "="*60)
    print("PODSUMOWANIE")
    print("="*60)
    for r in results:
        status = "Sukces" if r['success'] else "Blad"
        print(f"{status}: {r['series']}")

def main():
    print("\n" + "="*60)
    print("MASTER PARSER - Fiszki")
    print("="*60)
    
    available_series = check_series_availability()
    
    if not available_series:
        data_dir, parsers_dir = get_project_dirs()
        print("\nBrak dostepnych serii!")
        print("Upewnij sie, ze:")
        print(f"  1. Foldery w {data_dir}/<seria>/pdf/ zawieraja pliki PDF")
        print(f"  2. Parsery dla serii istnieja w {parsers_dir}/")
        print("\nAktualna struktura:")
        print(f"  Katalog danych: {data_dir}")
        print(f"  Katalog parserow: {parsers_dir}")
        if os.path.exists(data_dir):
            print(f"  Znalezione serie w data/: {os.listdir(data_dir)}")
        if os.path.exists(parsers_dir):
            parsers = [f for f in os.listdir(parsers_dir) if f.endswith('_parser.py')]
            print(f"  Znalezione parsery: {parsers if parsers else 'brak'}")
        return
    
    print("\nDostepne serie:")
    for idx, s in enumerate(available_series, 1):
        print(f"{idx}. {s['name']} ({s['pdf_count']} plikow PDF)")
    
    print(f"{len(available_series) + 1}. FULL AUTO - Parsuj wszystkie serie automatycznie")
    print("0. Wyjscie")
    
    while True:
        try:
            choice = int(input("\nWybierz opcje: "))
            
            if choice == 0:
                print("Zakonczono.")
                return
            
            if choice == len(available_series) + 1:
                full_auto_all_series()
                return
            
            if 1 <= choice <= len(available_series):
                series = available_series[choice - 1]
                print(f"\nUruchamianie parsera dla: {series['name']}")
                print(f"  Parser: {os.path.basename(series['parser'])}")
                print("\nParser uruchomi sie w trybie interaktywnym...")
                input("\nNacisnij Enter aby kontynuowac...")
                
                subprocess.run([sys.executable, series['parser']])
                return
            else:
                print("Nieprawidlowy wybor.")
        except ValueError:
            print("Wprowadz liczbe.")
        except KeyboardInterrupt:
            print("\n\nPrzerwano.")
            return

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrzerwano przez uzytkownika.")
    except Exception as e:
        print(f"\nBlad: {e}")
        import traceback
        traceback.print_exc()