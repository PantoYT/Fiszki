import fitz
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
pdf_path = os.path.join(project_root, "data", "new_enterprise_b1plus_wordlist_pl.pdf")

print(f"Szukam PDF w: {pdf_path}")
print(f"Czy istnieje? {os.path.exists(pdf_path)}")

if not os.path.exists(pdf_path):
    print("\nNie znaleziono pliku. Sprawdzam co jest w data/:")
    data_dir = os.path.join(project_root, "data")
    if os.path.exists(data_dir):
        print(os.listdir(data_dir))
    else:
        print("Folder data/ nie istnieje!")
    exit()

doc = fitz.open(pdf_path)
print(f"PDF ma {len(doc)} stron\n")
