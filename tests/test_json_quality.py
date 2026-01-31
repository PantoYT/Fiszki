#!/usr/bin/env python3
"""
JSON Quality Checker - Waliduje wszystkie JSON files pod kątem błędów
"""

import json
import os
from pathlib import Path
from collections import defaultdict


def check_json_structure(data, filename):
    """Sprawdza strukturę JSON'a"""
    issues = []
    
    if not isinstance(data, list):
        issues.append(f" Root nie jest array (to jest: {type(data).__name__})")
        return issues
    
    required_fields = {'word', 'unit'}
    optional_fields = {'pronunciation', 'part_of_speech', 'definition', 'translation', 
                       'error_rate', 'correct_count', 'wrong_count', 'sr_interval', 
                       'sr_repetitions', 'sr_ease', 'last_review'}
    
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            issues.append(f"  Entry #{i}: nie jest dict (to jest: {type(entry).__name__})")
            continue
        
        # Sprawdzaj required fields
        missing = required_fields - set(entry.keys())
        if missing:
            issues.append(f"  Entry #{i} (word: {entry.get('word', 'UNKNOWN')}): "
                         f"brakuje pól: {missing}")
        
        # Sprawdzaj typ word
        if 'word' in entry and not isinstance(entry['word'], str):
            issues.append(f"  Entry #{i}: 'word' powinien być string (to jest: {type(entry['word']).__name__})")
        
        # Sprawdzaj unknown fields
        unknown = set(entry.keys()) - required_fields - optional_fields
        if unknown:
            issues.append(f"  Entry #{i}: unknown fields: {unknown}")
    
    return issues


def check_duplicates(data, filename):
    """Sprawdza duplikaty słów"""
    issues = []
    seen = defaultdict(list)
    
    for i, entry in enumerate(data):
        if isinstance(entry, dict) and 'word' in entry and 'unit' in entry:
            key = (entry['word'].lower(), entry['unit'])
            seen[key].append(i)
    
    dupes = {k: v for k, v in seen.items() if len(v) > 1}
    if dupes:
        issues.append(f" Znaleziono {len(dupes)} duplikatów:")
        for (word, unit), indices in list(dupes.items())[:5]:  # First 5
            issues.append(f"  '{word}' (Unit: {unit}) - indices: {indices}")
        if len(dupes) > 5:
            issues.append(f"  ... i {len(dupes) - 5} więcej")
    
    return issues


def check_encoding(filepath):
    """Sprawdza czy plik ma UTF-8"""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            f.read()
    except UnicodeDecodeError as e:
        issues.append(f" Encoding problem: {e}")
    
    return issues


def check_file_size(filepath, data):
    """Sprawdza rozmiar pliku"""
    issues = []
    
    size_kb = os.path.getsize(filepath) / 1024
    word_count = len(data) if isinstance(data, list) else 0
    
    # Szacunkowy rozmiar: ~0.5KB per word
    expected_size = word_count * 0.5
    
    if size_kb > expected_size * 2:
        issues.append(f"  Plik większy niż oczekiwane ({size_kb:.1f}KB vs {expected_size:.1f}KB) - może mieć duplikaty")
    
    return issues


def check_all_json_files():
    """Main validator"""
    data_dir = Path("data")
    
    if not data_dir.exists():
        print(" data/ folder nie istnieje!")
        return
    
    print("\n" + "="*70)
    print("JSON QUALITY CHECK")
    print("="*70 + "\n")
    
    all_issues = {}
    all_stats = {}
    
    # New Enterprise
    ne_dir = data_dir / "new_enterprise" / "json"
    if ne_dir.exists():
        print("\n NEW ENTERPRISE")
        print("-" * 50)
        ne_stats = check_series(ne_dir, "new_enterprise")
        all_stats['new_enterprise'] = ne_stats
    
    # English File
    ef_dir = data_dir / "english_file" / "json"
    if ef_dir.exists():
        print("\n ENGLISH FILE")
        print("-" * 50)
        ef_stats = check_series(ef_dir, "english_file")
        all_stats['english_file'] = ef_stats
    
    # Career Paths
    cp_dir = data_dir / "career_paths"
    if cp_dir.exists():
        print("\n CAREER PATHS")
        print("-" * 50)
        cp_stats = check_career_paths(cp_dir)
        all_stats['career_paths'] = cp_stats
    
    # Summary
    print("\n" + "="*70)
    print(" SUMMARY")
    print("="*70)
    
    total_words = sum(stats['total'] for stats in all_stats.values())
    total_issues = sum(len(issues) for issues in all_issues.values())
    
    print(f"\n Total words across all series: {total_words:,}")
    print(f"  Total issues found: {total_issues}")
    
    if total_issues == 0:
        print("\n All JSON files are valid!")
    else:
        print("\n Issues need fixing!")


def check_series(series_dir, series_name):
    """Check all JSON files in a series"""
    stats = {'files': 0, 'total': 0, 'issues': 0}
    
    json_files = sorted(series_dir.glob("*.json"))
    
    if not json_files:
        print(f"  Brak JSON files w {series_dir}")
        return stats
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            issues = []
            issues.extend(check_encoding(json_file))
            issues.extend(check_json_structure(data, json_file.name))
            issues.extend(check_duplicates(data, json_file.name))
            issues.extend(check_file_size(json_file, data))
            
            word_count = len(data) if isinstance(data, list) else 0
            
            if issues:
                status = "" if any("" in i for i in issues) else ""
                print(f"{status} {json_file.name}: {word_count} words")
                for issue in issues[:3]:  # First 3 issues
                    print(f"   {issue}")
                if len(issues) > 3:
                    print(f"   ... i {len(issues) - 3} więcej")
                stats['issues'] += len(issues)
            else:
                print(f" {json_file.name}: {word_count} words - OK")
            
            stats['files'] += 1
            stats['total'] += word_count
        
        except json.JSONDecodeError as e:
            print(f" {json_file.name}: JSON decode error - {e}")
            stats['issues'] += 1
        except Exception as e:
            print(f" {json_file.name}: {e}")
            stats['issues'] += 1
    
    return stats


def check_career_paths(cp_dir):
    """Check all Career Paths categories"""
    stats = {'files': 0, 'total': 0, 'issues': 0}
    
    for category_dir in sorted(cp_dir.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith('.'):
            continue
        
        json_dir = category_dir / "json"
        if not json_dir.exists():
            continue
        
        json_files = list(json_dir.glob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                issues = []
                issues.extend(check_encoding(json_file))
                issues.extend(check_json_structure(data, json_file.name))
                issues.extend(check_duplicates(data, json_file.name))
                
                word_count = len(data) if isinstance(data, list) else 0
                
                if issues:
                    status = "" if any("" in i for i in issues) else ""
                    print(f"{status} {category_dir.name}/{json_file.name}: {word_count} words")
                    for issue in issues[:2]:
                        print(f"   {issue}")
                    stats['issues'] += len(issues)
                
                stats['files'] += 1
                stats['total'] += word_count
            
            except Exception as e:
                print(f" {category_dir.name}/{json_file.name}: {e}")
                stats['issues'] += 1
    
    return stats


if __name__ == "__main__":
    check_all_json_files()
