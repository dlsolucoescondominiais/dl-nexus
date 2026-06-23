import json

def dict_raise_on_duplicates(ordered_pairs):
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            raise ValueError(f"Duplicate key found: {k}")
        d[k] = v
    return d

def verify_json(file_path):
    print(f"[*] Verifying JSON validity and duplicate keys for {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Parse with strict duplicate key checking
        json.loads(content, object_pairs_hook=dict_raise_on_duplicates)
        print(f"[+] {file_path} is structurally VALID and has NO duplicate keys.")
    except ValueError as ve:
        print(f"[-] Duplicate key error in {file_path}: {ve}")
    except json.JSONDecodeError as jde:
        print(f"[-] JSON decode error in {file_path}: {jde}")
    except Exception as e:
        print(f"[-] Error: {e}")

verify_json("DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/001_TELEGRAM_RECEPCAO_ANINHA_V3.json")
verify_json("DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/002_roteador_aninha_v3_atendimento.json")
