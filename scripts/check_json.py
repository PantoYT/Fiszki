#!/usr/bin/env python3
"""JSON Quality Checker"""

import json
from pathlib import Path

def validate_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return True, len(data) if isinstance(data, list) else 0
    except Exception as e:
        return False, str(e)

def main():
    data_dir = Path("data")
    total_words = 0
    total_files = 0
    
    for json_file in sorted(data_dir.glob('**/json/*.json')):
        success, result = validate_json(json_file)
        if success:
            total_files += 1
            total_words += result
        else:
            print(f"ERROR: {json_file}: {result}")
    
    print(f"OK: {total_files} files, {total_words} words")

if __name__ == '__main__':
    main()

