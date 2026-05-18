from pathlib import Path

base = Path("DL_NEXUS_V3_LOCAL")

pastas = [
    "00_BACKUP_N8N",
    "01_WORKFLOWS_RECEBIDOS_JULES",
    "02_WORKFLOWS_REVISADOS_KILLCRITIC",
    "03_PROMPTS_AGENTES",
    "04_PAYLOADS_TESTE",
    "05_RELATORIOS",
    "06_HOSTGATOR_EMAIL",
    "07_SUPABASE_SCHEMA",
    "08_DOCUMENTACAO",
    "09_PRONTOS_PARA_PRODUCAO",
    "99_LIXEIRA_NAO_USAR"
]

print("Criando Zona de Quarentena DL Nexus V3...")

base.mkdir(exist_ok=True)

for pasta in pastas:
    caminho = base / pasta
    caminho.mkdir(parents=True, exist_ok=True)
    print(f"OK: {caminho}")

manual = """# MANUAL KILLCRITIC  DL NEXUS V3

Nada sobe para o n8n da HostGator sem passar por esta zona de quarentena.

REGRAS:
1. Nunca usar "visita técnica".
2. Usar sempre "Avaliação Técnica".
3. Nunca sugerir canaleta plástica como padrão.
4. Não misturar Setup com MRR.
5. Separar licença, SLA, peças e chamados avulsos.
6. A DL não atua como hidráulica pura.
7. Bombas e cisternas entram pelo escopo elétrico, comando, automação, proteção e monitoramento.
8. JSON recebido do Jules entra em 01_WORKFLOWS_RECEBIDOS_JULES.
9. JSON aprovado vai para 09_PRONTOS_PARA_PRODUCAO.
"""

(base / "MANUAL_KILLCRITIC.md").write_text(manual, encoding="utf-8")

print("ZONA DE QUARENTENA ESTABELECIDA COM SUCESSO.")
