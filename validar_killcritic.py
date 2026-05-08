import json
import sys

def validate(filepath):
    forbidden = ["visita técnica", "canaleta plástica", "manutenção hidráulica pura"]

    with open(filepath, 'r') as f:
        content = f.read().lower()

    for term in forbidden:
        if term in content:
            print(f"FAILED: The forbidden term '{term}' was found in {filepath}.")
            sys.exit(1)

    print("OK: No forbidden terms found.")

if __name__ == "__main__":
    validate(sys.argv[1])
