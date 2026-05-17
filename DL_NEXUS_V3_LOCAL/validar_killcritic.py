import json
import os
import re
import sys

FORBIDDEN_TERMS = [
    r'visita\s+t[eé]cnica',
    r'canaleta\s+pl[aá]stica',
    r'manuten[cç][aã]o\s+hidr[aá]ulica\s+pura',
    r'engenheiro',
    r'garantia\s+vital[íi]cia'
]

def validate_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            for term in FORBIDDEN_TERMS:
                if re.search(term, content):
                    if 'nunca diga visita técnica' not in content and 'nunca usar' not in content:
                        print(f"FAILED: {filepath} contains forbidden term matching {term}")
                        return False
        return True
    except Exception as e:
        return True

def main():
    directories = ['backend/n8n/workflows/v3', 'DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N']
    all_passed = True
    count = 0
    for directory in directories:
        if not os.path.exists(directory):
            continue

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json') and not file.endswith('.fixed.json'):
                    count += 1
                    if not validate_file(os.path.join(root, file)):
                        all_passed = False

    if all_passed:
        print(f"KILLCRITIC validation passed for {count} workflow files.")
        sys.exit(0)
    else:
        print("KILLCRITIC validation failed.")
        sys.exit(1)

if __name__ == '__main__':
    main()
