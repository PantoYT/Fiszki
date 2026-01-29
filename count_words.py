import json
import glob

ne_words = 0
for f in glob.glob('data/new_enterprise/json/*.json'):
    with open(f, 'r', encoding='utf-8') as file:
        ne_words += len(json.load(file))

ef_words = 0
for f in glob.glob('data/english_file/json/*.json'):
    with open(f, 'r', encoding='utf-8') as file:
        ef_words += len(json.load(file))

cp_words = 0
for f in glob.glob('data/career_paths/*/json/*.json'):
    with open(f, 'r', encoding='utf-8') as file:
        cp_words += len(json.load(file))

print(f'New Enterprise: {ne_words}')
print(f'English File: {ef_words}')
print(f'Career Paths: {cp_words}')
print(f'TOTAL: {ne_words + ef_words + cp_words}')
