import json
import os
import re
import sys

FORBIDDEN_TERMS = [
    r'visita\s+t[eé]cnica',
    r'canaleta\s+pl[aá]stica',
    r'manuten[cç][aã]o\s+hidr[aá]ulica\s+pura',
    r'engenheiro'
]

def validate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().lower()
        for term in FORBIDDEN_TERMS:
            if re.search(term, content):
                # allow negative constraints or valid usages
                if 'nunca diga visita técnica' not in content and 'nunca usar' not in content:
                    print(f"FAILED: {filepath} contains forbidden term matching {term}")
                    return False
    print(f"PASSED: {filepath}")
    return True

def main():
    directory = 'DL_NEXUS_V3_LOCAL'
    all_passed = True
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                if not validate_file(os.path.join(root, file)):
                    all_passed = False

    if all_passed:
        print("KILLCRITIC validation passed.")
        sys.exit(0)
    else:
        print("KILLCRITIC validation failed.")
        sys.exit(1)

if __name__ == '__main__':
    main()
