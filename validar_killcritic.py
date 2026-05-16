import json
import glob
import sys
import os

FORBIDDEN_TERMS = ["visita técnica", "canaleta plástica", "manutenção hidráulica pura"]
EXCEPTIONS = ["nunca diga visita técnica", "nunca usar visita técnica"]

def validate_json_files(path_pattern):
    has_errors = False
    files = glob.glob(path_pattern, recursive=True)

    if not files:
        print(f"No files found matching {path_pattern}")
        return False

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            content_lower = content.lower()

            # Temporarily replace exceptions with placeholder so they aren't caught
            for exception in EXCEPTIONS:
                content_lower = content_lower.replace(exception, "---exception---")

            file_errors = []

            for term in FORBIDDEN_TERMS:
                if term in content_lower:
                    file_errors.append(term)

            if file_errors:
                print(f"ERROR: {file_path} contains forbidden terms: {', '.join(file_errors)}")
                has_errors = True
            else:
                print(f"OK: {file_path}")

        except json.JSONDecodeError:
            print(f"ERROR: {file_path} is not valid JSON")
            has_errors = True
        except Exception as e:
            print(f"ERROR reading {file_path}: {e}")
            has_errors = True

    return has_errors

if __name__ == "__main__":
    if validate_json_files("backend/n8n/workflows/**/*.json"):
        sys.exit(1)
    else:
        print("All JSON files passed Killcritic validation.")
        sys.exit(0)
