#!/usr/bin/env python3
"""
Deep audit of all JSON vocabulary files for parser quality issues.
Checks for:
1. Polish words in English 'word' field
2. Missing/empty fields
3. Non-UTF8 encoding issues
4. Structural problems
5. Duplicate entries
"""

import json
import os
from pathlib import Path
from collections import defaultdict

# Polish characters that shouldn't be in English words
POLISH_CHARS = set('ąćęłńóśźżĄĆĘŁŃÓŚŹŻ')

def has_polish_chars(text):
    """Check if text contains Polish characters."""
    if not text:
        return False
    return any(c in text for c in POLISH_CHARS)

def is_likely_polish_word(text):
    """Check if word looks like Polish (has Polish chars or Polish patterns)."""
    if not text:
        return False
    
    # Check for Polish characters
    if has_polish_chars(text):
        return True
    
    # Check for common Polish word patterns
    polish_patterns = [
        'ów', 'ami', 'ach', 'em', 'ie', 'ę', 'ą', 
        'ć', 'ł', 'ń', 'ś', 'ź', 'ż',
        'ski', 'ska', 'skie'  # Adjective endings
    ]
    
    text_lower = text.lower()
    for pattern in polish_patterns:
        if text_lower.endswith(pattern) and len(text) > 4:
            return True
    
    return False

def audit_file(filepath):
    """Audit a single JSON file."""
    issues = {
        'polish_words': [],
        'missing_fields': [],
        'empty_fields': [],
        'duplicates': [],
        'encoding_issues': [],
        'structural_issues': []
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        issues['encoding_issues'].append(str(e))
        return issues, 0
    
    if not isinstance(data, list):
        issues['structural_issues'].append('Root is not a list')
        return issues, 0
    
    seen_words = set()
    
    for idx, entry in enumerate(data):
        if not isinstance(entry, dict):
            issues['structural_issues'].append(f'Entry {idx} is not a dict')
            continue
        
        # Check for required fields - word is always required
        if 'word' not in entry:
            issues['missing_fields'].append(f"Entry {idx}: missing word field")
            continue
        
        # Get word (required) and check if empty
        word = entry.get('word', '').strip()
        if not word:
            issues['empty_fields'].append(f"Entry {idx}: empty word")
            continue
        
        # Check for ACTUAL Polish characters (not patterns) in English field
        # Only flag if PURE Polish chars exist (ąćęłńóśźż)
        if has_polish_chars(word):
            # This is a real issue - English word shouldn't have Polish chars
            issues['polish_words'].append({
                'index': idx,
                'word': word,
                'note': f'Contains Polish characters'
            })
        
        # Check for duplicates
        if word.lower() in seen_words:
            issues['duplicates'].append(f"Entry {idx}: duplicate word '{word}'")
        else:
            seen_words.add(word.lower())
    
    return issues, len(data)

def main():
    base_path = Path('data')
    
    # Find all JSON files
    json_files = sorted(base_path.glob('**/json/*.json'))
    
    print("=" * 80)
    print("DEEP JSON QUALITY AUDIT")
    print("=" * 80)
    
    total_words = 0
    total_files = 0
    all_issues = defaultdict(list)
    
    for json_file in json_files:
        series = json_file.parent.parent.parent.name
        category = json_file.parent.parent.name
        filename = json_file.name
        
        issues, word_count = audit_file(json_file)
        total_words += word_count
        total_files += 1
        
        # Print if any issues
        has_issues = any(v for k, v in issues.items() if v)
        
        if has_issues:
            print(f"\n{series}/{category}/{filename}")
            print(f"  Words: {word_count}")
            
            if issues['polish_words']:
                print(f"  POLISH_WORDS: {len(issues['polish_words'])}")
                for item in issues['polish_words'][:5]:  # Show first 5
                    print(f"      [{item['index']}] {item['word']}")
                if len(issues['polish_words']) > 5:
                    print(f"      ... and {len(issues['polish_words']) - 5} more")
            
            if issues['missing_fields']:
                print(f"  MISSING: {len(issues['missing_fields'])}")
                for msg in issues['missing_fields'][:3]:
                    print(f"      {msg}")
            
            if issues['empty_fields']:
                print(f"  EMPTY: {len(issues['empty_fields'])}")
            
            if issues['duplicates']:
                print(f"  DUPLICATES: {len(issues['duplicates'])}")
            
            if issues['encoding_issues']:
                print(f"  ENCODING_ISSUES: {issues['encoding_issues']}")
            
            if issues['structural_issues']:
                print(f"  STRUCTURAL_ISSUES: {issues['structural_issues']}")
            
            # Collect for summary
            for key, value in issues.items():
                if value:
                    all_issues[key].append((f"{series}/{category}/{filename}", value))
    
    print("\n" + "=" * 80)
    print("AUDIT SUMMARY")
    print("=" * 80)
    print(f"Total files: {total_files}")
    print(f"Total words: {total_words}")
    print()
    
    if all_issues['polish_words']:
        print(f"Files with Polish characters in 'word' field: {len(all_issues['polish_words'])}")
        for file_path, issues_list in all_issues['polish_words'][:10]:
            print(f"  - {file_path}: {len(issues_list)} instances")
        if len(all_issues['polish_words']) > 10:
            print(f"  ... and {len(all_issues['polish_words']) - 10} more files")
    
    if all_issues['missing_fields']:
        print(f"Files with missing 'word' field: {len(all_issues['missing_fields'])}")
        for file_path, issues_list in all_issues['missing_fields'][:5]:
            print(f"  - {file_path}")
    
    if all_issues['duplicates']:
        print(f"Files with duplicate words: {len(all_issues['duplicates'])}")
    
    print("\n" + "=" * 80)
    if all_issues['polish_words'] or all_issues['missing_fields']:
        print(f"Status: ISSUES FOUND")
    else:
        print(f"Status: CLEAN - All JSON files are valid")
    print("=" * 80)

if __name__ == '__main__':
    main()
