#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║  DL NEXUS — Engine de Sincronização n8n ↔ Git ↔ Supabase   ║
║  Empresa: DL Soluções Condominiais LTDA | CREA-RJ           ║
║  Autor: Antigravity Agent                                    ║
║  Data: 2026-04-23                                            ║
╚══════════════════════════════════════════════════════════════╝

USO:
    python n8n_sync.py --validate              # Valida JSONs locais
    python n8n_sync.py --pull --dry-run         # Mostra diff sem alterar (futuro)
    python n8n_sync.py --push --workflow 001    # Envia workflow específico (futuro)
    python n8n_sync.py --export-git             # Prepara arquivos para git commit
    python n8n_sync.py --log-supabase           # Registra operação no Supabase
"""

import argparse
import json
import logging
import os
import sys
import hashlib
import difflib
from datetime import datetime
from pathlib import Path
from typing import Optional

# ═══════════════════════════════════════
# CONFIGURAÇÃO
# ═══════════════════════════════════════

# Paths relativos ao repositório
REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = REPO_ROOT / "backend" / "n8n" / "workflows"
EXECUTION_WORKFLOWS_DIR = REPO_ROOT / "execution" / "n8n_workflows"

# n8n API (futuro - quando VPS estiver online)
N8N_HOST = os.getenv("N8N_HOST", "https://n8n.dlsolucoescondominiais.com.br/api/v1")
N8N_API_KEY = os.getenv("N8N_API_KEY", "")

# Supabase (para logging)
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

# Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("dl_nexus_sync")

# ═══════════════════════════════════════
# REGRAS DE SEGURANÇA (Hard Rules)
# ═══════════════════════════════════════

# Padrões que NUNCA devem aparecer em workflows versionados
SECURITY_PATTERNS = [
    "sk_",          # ElevenLabs
    "sk-",          # OpenAI
    "eyJhbGci",     # JWT tokens raw
    "Bearer ",      # Auth headers com token real
    "password",     # Senhas literais
]

# Campos de credenciais que são aceitáveis (referência do n8n, não o secret real)
SAFE_CREDENTIAL_REFS = [
    '"id":', '"name":',  # Referências de credential ID do n8n
    "$env.",              # Variáveis de ambiente do n8n
    "{{ $env.",           # Template de variável n8n
]


# ═══════════════════════════════════════
# FUNÇÕES DE VALIDAÇÃO
# ═══════════════════════════════════════

def validate_json_structure(filepath: Path) -> dict:
    """Valida se um arquivo JSON de workflow n8n é válido e seguro."""
    result = {
        "file": filepath.name,
        "valid_json": False,
        "has_nodes": False,
        "has_connections": False,
        "security_ok": True,
        "security_issues": [],
        "node_count": 0,
        "workflow_name": "",
    }

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        result["valid_json"] = True
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON inválido em {filepath.name}: {e}")
        return result
    except Exception as e:
        logger.error(f"❌ Erro ao ler {filepath.name}: {e}")
        return result

    # Validar estrutura mínima de workflow n8n
    result["has_nodes"] = "nodes" in data and isinstance(data["nodes"], list)
    result["has_connections"] = "connections" in data and isinstance(data["connections"], dict)
    result["workflow_name"] = data.get("name", "SEM NOME")
    result["node_count"] = len(data.get("nodes", []))

    # Scan de segurança — buscar secrets hardcoded
    raw_content = json.dumps(data)
    for pattern in SECURITY_PATTERNS:
        if pattern in raw_content:
            # Verificar se é uma referência segura ou um leak real
            is_safe = False
            for safe in SAFE_CREDENTIAL_REFS:
                if safe in raw_content:
                    # Heurística: se contém referência de env var, provavelmente é seguro
                    pass
            
            # Buscar a linha exata do leak
            lines_with_pattern = []
            for i, line in enumerate(json.dumps(data, indent=2).split("\n")):
                if pattern in line:
                    # Verificar se está dentro de um $env reference
                    if "$env." not in line and "{{ $env." not in line:
                        lines_with_pattern.append(f"  L{i+1}: {line.strip()}")
            
            if lines_with_pattern:
                result["security_ok"] = False
                result["security_issues"].append({
                    "pattern": pattern,
                    "locations": lines_with_pattern
                })

    return result


def validate_all_workflows() -> list:
    """Valida todos os workflows JSON no diretório padrão."""
    results = []
    
    for directory in [WORKFLOWS_DIR, EXECUTION_WORKFLOWS_DIR]:
        if not directory.exists():
            logger.warning(f"⚠️ Diretório não encontrado: {directory}")
            continue
            
        for json_file in sorted(directory.glob("*.json")):
            logger.info(f"🔍 Validando: {json_file.relative_to(REPO_ROOT)}")
            result = validate_json_structure(json_file)
            results.append(result)
            
            if result["valid_json"]:
                status = "✅" if result["security_ok"] else "🔴 SECURITY LEAK"
                logger.info(
                    f"  {status} | {result['workflow_name']} | "
                    f"{result['node_count']} nós"
                )
                if not result["security_ok"]:
                    for issue in result["security_issues"]:
                        logger.error(f"  🚨 Padrão detectado: '{issue['pattern']}'")
                        for loc in issue["locations"]:
                            logger.error(f"    {loc}")
            else:
                logger.error(f"  ❌ JSON CORROMPIDO: {json_file.name}")
    
    return results


# ═══════════════════════════════════════
# FUNÇÕES DE INVENTÁRIO
# ═══════════════════════════════════════

def get_local_inventory() -> dict:
    """Gera inventário dos workflows locais com hash para detecção de mudanças."""
    inventory = {}
    
    for directory in [WORKFLOWS_DIR, EXECUTION_WORKFLOWS_DIR]:
        if not directory.exists():
            continue
        for json_file in sorted(directory.glob("*.json")):
            with open(json_file, "rb") as f:
                content = f.read()
            
            md5 = hashlib.md5(content).hexdigest()
            try:
                data = json.loads(content)
                name = data.get("name", json_file.stem)
            except Exception:
                name = json_file.stem
            
            inventory[json_file.name] = {
                "path": str(json_file.relative_to(REPO_ROOT)),
                "name": name,
                "md5": md5,
                "size_bytes": len(content),
                "last_modified": datetime.fromtimestamp(
                    json_file.stat().st_mtime
                ).isoformat(),
            }
    
    return inventory


def show_inventory():
    """Mostra o inventário completo dos workflows locais."""
    inventory = get_local_inventory()
    
    logger.info("=" * 65)
    logger.info("📋 INVENTÁRIO DE WORKFLOWS — DL NEXUS")
    logger.info("=" * 65)
    
    for filename, info in inventory.items():
        logger.info(
            f"  📄 {filename}\n"
            f"     Nome: {info['name']}\n"
            f"     Path: {info['path']}\n"
            f"     MD5:  {info['md5']}\n"
            f"     Size: {info['size_bytes']} bytes\n"
            f"     Mod:  {info['last_modified']}"
        )
    
    logger.info(f"\n  Total: {len(inventory)} workflows")
    return inventory


# ═══════════════════════════════════════
# FUNÇÕES DE SYNC n8n API (FUTURO)
# ═══════════════════════════════════════

def _get_n8n_headers() -> dict:
    """Headers de autenticação para a API do n8n."""
    if not N8N_API_KEY:
        logger.error("❌ N8N_API_KEY não configurada no .env")
        sys.exit(1)
    return {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json",
    }


def pull_from_n8n(dry_run: bool = True):
    """
    [FUTURO] Puxa workflows do n8n remoto e salva localmente.
    Requer VPS online e API acessível.
    """
    try:
        import requests
    except ImportError:
        logger.error("❌ Instale requests: pip install requests")
        return

    logger.info(f"🔄 Conectando ao n8n: {N8N_HOST}")
    
    try:
        resp = requests.get(
            f"{N8N_HOST}/workflows",
            headers=_get_n8n_headers(),
            timeout=15
        )
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        logger.error(
            "❌ n8n não acessível. A VPS está online?\n"
            "   URL: {N8N_HOST}\n"
            "   Dica: Use --validate para validar workflows locais."
        )
        return
    except Exception as e:
        logger.error(f"❌ Erro na API do n8n: {e}")
        return

    workflows = resp.json().get("data", [])
    logger.info(f"📥 {len(workflows)} workflows encontrados no n8n remoto")

    for wf in workflows:
        wf_id = wf.get("id", "unknown")
        wf_name = wf.get("name", "unnamed")
        
        # Buscar detalhes completos do workflow
        detail_resp = requests.get(
            f"{N8N_HOST}/workflows/{wf_id}",
            headers=_get_n8n_headers(),
            timeout=15
        )
        detail_resp.raise_for_status()
        wf_data = detail_resp.json()

        # Gerar nome de arquivo sanitizado
        safe_name = wf_name.replace(" ", "_").replace("/", "_")
        target_file = WORKFLOWS_DIR / f"{safe_name}.json"

        if dry_run:
            if target_file.exists():
                # Mostrar diff
                with open(target_file, "r", encoding="utf-8") as f:
                    local_content = f.read()
                remote_content = json.dumps(wf_data, indent=2, ensure_ascii=False)
                
                diff = list(difflib.unified_diff(
                    local_content.splitlines(),
                    remote_content.splitlines(),
                    fromfile=f"LOCAL: {target_file.name}",
                    tofile=f"REMOTO: {wf_name}",
                    lineterm=""
                ))
                
                if diff:
                    logger.info(f"📝 DIFF detectado: {target_file.name}")
                    for line in diff[:30]:  # Limitar output
                        print(line)
                else:
                    logger.info(f"✅ Sem diferenças: {target_file.name}")
            else:
                logger.info(f"🆕 Novo workflow: {wf_name} → {target_file.name}")
        else:
            # Salvar arquivo local
            with open(target_file, "w", encoding="utf-8") as f:
                json.dump(wf_data, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Salvo: {target_file.name}")

    logger.info("✅ Pull concluído")


def push_to_n8n(workflow_filter: Optional[str] = None, dry_run: bool = True):
    """
    [FUTURO] Envia workflows locais para o n8n remoto.
    Requer VPS online e API acessível.
    """
    try:
        import requests
    except ImportError:
        logger.error("❌ Instale requests: pip install requests")
        return

    logger.info(f"🔄 Preparando push para n8n: {N8N_HOST}")
    
    for json_file in sorted(WORKFLOWS_DIR.glob("*.json")):
        if workflow_filter and workflow_filter not in json_file.name:
            continue
        
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        wf_name = data.get("name", json_file.stem)
        
        # Validar segurança antes de enviar
        validation = validate_json_structure(json_file)
        if not validation["security_ok"]:
            logger.error(f"🚫 BLOQUEADO: {json_file.name} contém secrets hardcoded")
            continue
        
        if dry_run:
            logger.info(f"📤 [DRY-RUN] Enviaria: {json_file.name} ({wf_name})")
        else:
            try:
                # Tentar atualizar existente ou criar novo
                resp = requests.post(
                    f"{N8N_HOST}/workflows",
                    headers=_get_n8n_headers(),
                    json=data,
                    timeout=30
                )
                if resp.status_code in (200, 201):
                    logger.info(f"✅ Enviado: {wf_name}")
                else:
                    logger.error(
                        f"❌ Erro ao enviar {wf_name}: "
                        f"{resp.status_code} - {resp.text[:200]}"
                    )
            except Exception as e:
                logger.error(f"❌ Falha no push de {wf_name}: {e}")

    logger.info("✅ Push concluído")


# ═══════════════════════════════════════
# FUNÇÕES DE SYNC GIT (MODO ATUAL)
# ═══════════════════════════════════════

def export_for_git():
    """
    Prepara o estado dos workflows para commit.
    Gera um relatório de mudanças e os comandos git exatos.
    """
    inventory = get_local_inventory()
    validation = validate_all_workflows()
    
    # Contar resultados
    total = len(validation)
    valid = sum(1 for v in validation if v["valid_json"])
    secure = sum(1 for v in validation if v["security_ok"])
    
    logger.info("\n" + "=" * 65)
    logger.info("📊 RELATÓRIO DE SYNC — PRONTO PARA GIT")
    logger.info("=" * 65)
    logger.info(f"  Workflows encontrados: {total}")
    logger.info(f"  JSON válido:           {valid}/{total}")
    logger.info(f"  Segurança OK:          {secure}/{total}")
    
    if secure < total:
        logger.error("\n🚫 SYNC BLOQUEADO — Corrija os security leaks antes do commit!")
        for v in validation:
            if not v["security_ok"]:
                logger.error(f"  → {v['file']}: {len(v['security_issues'])} problemas")
        return False
    
    # Gerar comandos git
    logger.info("\n📋 COMANDOS GIT (execute no seu terminal nativo):")
    logger.info("-" * 50)
    print(f"""
# === DL NEXUS SYNC — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===
cd {REPO_ROOT}

# Stage dos workflows n8n
git add backend/n8n/workflows/*.json
git add execution/n8n_workflows/*.json
git add .gitignore

# Commit com mensagem padronizada
git commit -m "sync(n8n): {total} workflows validados | {datetime.now().strftime('%Y-%m-%d')}"

# Push para o repositório remoto
git push origin main
""")
    
    return True


# ═══════════════════════════════════════
# LOGGING SUPABASE (AUDITORIA)
# ═══════════════════════════════════════

def log_to_supabase(componente: str, acao: str, detalhes: dict):
    """Registra operação de sync na tabela dl_sync_log do Supabase."""
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        logger.warning("⚠️ Supabase não configurado. Log ignorado.")
        return
    
    try:
        import requests
    except ImportError:
        logger.warning("⚠️ requests não instalado. Log Supabase ignorado.")
        return
    
    payload = {
        "componente": componente,
        "acao": acao,
        "detalhes": detalhes,
        "status": "ok"
    }
    
    try:
        resp = requests.post(
            f"{SUPABASE_URL}/rest/v1/dl_sync_log",
            headers={
                "apikey": SUPABASE_SERVICE_ROLE_KEY,
                "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            },
            json=payload,
            timeout=10
        )
        if resp.status_code in (200, 201, 204):
            logger.info("📝 Log registrado no Supabase")
        else:
            logger.warning(f"⚠️ Supabase log falhou: {resp.status_code}")
    except Exception as e:
        logger.warning(f"⚠️ Supabase log falhou: {e}")


# ═══════════════════════════════════════
# CLI — INTERFACE DE LINHA DE COMANDO
# ═══════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="DL Nexus — Engine de Sincronização n8n ↔ Git ↔ Supabase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python n8n_sync.py --validate              Valida todos os JSONs
  python n8n_sync.py --inventory             Mostra inventário completo
  python n8n_sync.py --export-git            Prepara para git commit
  python n8n_sync.py --pull --dry-run        [FUTURO] Diff do n8n remoto
  python n8n_sync.py --push --workflow 001   [FUTURO] Deploy de workflow
        """
    )
    
    # Modos de operação
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--validate", action="store_true",
                       help="Valida a estrutura e segurança de todos os workflows JSON")
    group.add_argument("--inventory", action="store_true",
                       help="Mostra inventário completo com hashes MD5")
    group.add_argument("--export-git", action="store_true",
                       help="Prepara workflows para commit Git (modo atual)")
    group.add_argument("--pull", action="store_true",
                       help="[FUTURO] Puxa workflows do n8n remoto")
    group.add_argument("--push", action="store_true",
                       help="[FUTURO] Envia workflows para o n8n remoto")
    
    # Opções
    parser.add_argument("--dry-run", action="store_true",
                        help="Simula a operação sem efetuar mudanças")
    parser.add_argument("--workflow", type=str, default=None,
                        help="Filtrar por nome de workflow (ex: 001, aninha)")
    parser.add_argument("--log", action="store_true",
                        help="Registra a operação no Supabase (tabela dl_sync_log)")
    
    args = parser.parse_args()
    
    logger.info("╔══════════════════════════════════════════╗")
    logger.info("║  DL NEXUS — Sync Engine v1.0             ║")
    logger.info("║  DL Soluções Condominiais LTDA            ║")
    logger.info("╚══════════════════════════════════════════╝")
    
    if args.validate:
        results = validate_all_workflows()
        if args.log:
            log_to_supabase("n8n", "validate", {
                "total": len(results),
                "valid": sum(1 for r in results if r["valid_json"]),
                "secure": sum(1 for r in results if r["security_ok"]),
            })
    
    elif args.inventory:
        show_inventory()
    
    elif args.export_git:
        success = export_for_git()
        if success and args.log:
            inventory = get_local_inventory()
            log_to_supabase("n8n", "export_git", {
                "workflows": len(inventory),
                "timestamp": datetime.now().isoformat(),
            })
    
    elif args.pull:
        pull_from_n8n(dry_run=args.dry_run)
        if args.log:
            log_to_supabase("n8n", "pull", {"dry_run": args.dry_run})
    
    elif args.push:
        push_to_n8n(workflow_filter=args.workflow, dry_run=args.dry_run)
        if args.log:
            log_to_supabase("n8n", "push", {
                "dry_run": args.dry_run,
                "filter": args.workflow,
            })


if __name__ == "__main__":
    main()
