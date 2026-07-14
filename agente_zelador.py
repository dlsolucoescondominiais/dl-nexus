import os
import shutil
import re
import datetime
import json
from pathlib import Path

# --- CONFIGURACAO ---
BASE_DIR = Path("DL_NEXUS_DRIVE")
LOG_DIR = BASE_DIR / "05_AUTOMACAO" / "LOGS"
LOG_FILE = LOG_DIR / "RELATORIO_ZELADOR_DRIVE.md"
STATE_FILE = LOG_DIR / "zelador_state.json"

STRUCTURE = {
    "00_INBOX": [],
    "01_COMERCIAL": ["PROPOSTAS", "ORCAMENTOS", "CONTRATOS"],
    "02_TECNICO": ["RELATORIOS", "PROJETOS"],
    "03_CLIENTES": ["CONDOMINIOS", "EMPRESAS", "RESTAURANTES"],
    "04_MARKETING": ["IMAGENS", "VIDEOS"],
    "05_AUTOMACAO": ["N8N", "JSON", "PROMPTS", "LOGS"],
    "06_DL_ACQUA": [],
    "07_BACKUP_CONTROLADO": [],
    "99_ARQUIVO_MORTO": []
}

# Regex to clean up the name
REGEX_COPIA_DE = re.compile(r'(?i)c[óo]pia\s+de\s+')
REGEX_UNTITLED = re.compile(r'(?i)untitled')
REGEX_INVALID_CHARS = re.compile(r'[^\w\s\-]')

# --- INICIALIZACAO ---
def init_structure():
    if not BASE_DIR.exists():
        BASE_DIR.mkdir()
    for main_folder, subfolders in STRUCTURE.items():
        (BASE_DIR / main_folder).mkdir(exist_ok=True)
        for sub in subfolders:
            (BASE_DIR / main_folder / sub).mkdir(exist_ok=True)

# --- CLASSIFICACAO ---
def classify_file(filename):
    lower_name = filename.lower()

    # BACKUP CRÍTICO (PRIORIDADE 1)
    if any(keyword in lower_name for keyword in ["msgstore", "crypt", "whatsapp", "backup", ".db"]):
        return "07_BACKUP_CONTROLADO", None, "BACKUP"

    # AUTOMAÇÃO (PRIORIDADE 2)
    if any(keyword in lower_name for keyword in [".json", "workflow", "n8n", "prompt", "agent"]):
        return "05_AUTOMACAO", None, "AUTOMACAO"

    # COMERCIAL (PRIORIDADE 3)
    if "proposta" in lower_name: return "01_COMERCIAL", "PROPOSTAS", "PROPOSTA"
    if "orçamento" in lower_name or "orcamento" in lower_name: return "01_COMERCIAL", "ORCAMENTOS", "ORCAMENTO"
    if "contrato" in lower_name: return "01_COMERCIAL", "CONTRATOS", "CONTRATO"

    # TÉCNICO (PRIORIDADE 4)
    if "relatório" in lower_name or "relatorio" in lower_name: return "02_TECNICO", "RELATORIOS", "RELATORIO"
    if "projeto" in lower_name: return "02_TECNICO", "PROJETOS", "PROJETO"
    if any(keyword in lower_name for keyword in ["técnico", "tecnico", "elétrica", "eletrica", "cftv"]): return "02_TECNICO", None, "TECNICO"

    # CLIENTES (PRIORIDADE 5)
    if any(keyword in lower_name for keyword in ["palazzo", "tecval", "condomínio", "condominio", "edifício", "edificio", "cliente"]):
        return "03_CLIENTES", None, "CLIENTE"

    # MARKETING (PRIORIDADE 6)
    if any(keyword in lower_name for keyword in [".jpg", ".png", ".jpeg", "imagem"]): return "04_MARKETING", "IMAGENS", "IMAGEM"
    if any(keyword in lower_name for keyword in [".mp4", "vídeo", "video"]): return "04_MARKETING", "VIDEOS", "VIDEO"

    # DL ACQUA (PRIORIDADE 7)
    if any(keyword in lower_name for keyword in ["água", "agua", "cisterna", "reservatório", "reservatorio", "consumo", "dashboard"]):
        return "06_DL_ACQUA", None, "ACQUA"

    # ARQUIVO SUJO (PRIORIDADE FINAL)
    if any(keyword in lower_name for keyword in ["untitled", "sem nome", "cópia de", "copia de"]):
        return "99_ARQUIVO_MORTO", None, "ARQUIVO"

    return "00_INBOX", None, "INBOX"

# --- RENOMEACAO ---
def rename_file(filename, tipo, doc_type=""):
    if filename.startswith("DL_") and re.search(r'_\d{4}-\d{2}\.', filename):
        return filename # Já está no padrão

    ext = os.path.splitext(filename)[1]
    name = os.path.splitext(filename)[0]

    name = REGEX_COPIA_DE.sub('', name)
    name = REGEX_UNTITLED.sub('', name)
    name = REGEX_INVALID_CHARS.sub('', name)

    name = name.strip().upper().replace(' ', '_')
    if not name:
        name = "ARQUIVO"

    now = datetime.datetime.now().strftime("%Y-%m")

    new_name = f"DL_{tipo}_{name}_{now}{ext}"
    return new_name

# --- EXECUCAO ---
def run():
    init_structure()

    stats = {
        "analisados": 0,
        "movidos": 0,
        "renomeados": 0,
        "erros": 0,
        "conflitos": 0,
        "nao_classificados": 0
    }

    # Controle de estado para ignorar arquivos com erro persistente
    state = {"erros_ignorados": []}
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
        except:
            pass

    files_to_process = []

    # Buscar arquivos que não estão formatados com DL_ ou que estão no INBOX
    for root, _, files in os.walk(BASE_DIR):
        if "05_AUTOMACAO" in root and "LOGS" in root: continue # dont process logs
        for file in files:
            file_path = Path(root) / file
            # Pular se estiver no estado de erro para não loopar
            if str(file_path) in state.get("erros_ignorados", []):
                continue

            # Se não começa com DL_, precisa processar
            if not file.startswith("DL_"):
                files_to_process.append(file_path)
            # Ou se está no INBOX mas a gente já rodou? Vamos focar só nos que não têm padrão DL_
            elif "00_INBOX" in root:
                # Se está no INBOX e tem DL_, podemos tentar classificar de novo?
                pass

    total_pendentes = max(0, len(files_to_process) - 50)
    # Lote de 50
    files_to_process = files_to_process[:50]

    for file_path in files_to_process:
        stats["analisados"] += 1

        main_folder, sub_folder, file_type = classify_file(file_path.name)

        if main_folder == "00_INBOX":
            stats["nao_classificados"] += 1

        new_name = rename_file(file_path.name, file_type)

        dest_dir = BASE_DIR / main_folder
        if sub_folder:
            dest_dir = dest_dir / sub_folder

        dest_path = dest_dir / new_name

        try:
            # Killcritic protection check: não sobrescrever nem excluir
            # Mover é permitido. O script não altera conteúdo de nenhum arquivo internamente.
            if file_path != dest_path:
                if dest_path.exists():
                     stats["conflitos"] += 1
                     now_ms = datetime.datetime.now().strftime("%f")
                     dest_path = dest_dir / f"{dest_path.stem}_{now_ms}{dest_path.suffix}"

                shutil.move(str(file_path), str(dest_path))
                stats["movidos"] += 1
                if file_path.name != dest_path.name:
                    stats["renomeados"] += 1

        except Exception as e:
            stats["erros"] += 1
            state["erros_ignorados"].append(str(file_path))

    # Salvar estado
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f)

    # GERAR LOG
    log_content = f"""# RELATORIO_ZELADOR_DRIVE

- total de arquivos analisados: {stats['analisados']}
- arquivos movidos: {stats['movidos']}
- arquivos renomeados: {stats['renomeados']}
- conflitos: {stats['conflitos']}
- não classificados: {stats['nao_classificados']}
- erros: {stats['erros']}
"""
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write(log_content)

    print(f"""STATUS: CONCLUIDO
PROCESSADOS: {stats['analisados']}
RENOMEADOS: {stats['renomeados']}
MOVIDOS: {stats['movidos']}
ERROS: {stats['erros']}
PENDENTES: {total_pendentes}""")

if __name__ == "__main__":
    run()
