import os

scripts = [
    'gerar_manus_prospeccao.py',
    'linkar_manus_marketing.py',
    'linkar_manus_marketing_v2.py',
    'linkar_manus_marketing_v3.py',
    'deploy_manus_070.py',
    'scripts/rebuild_070_manus_real.py',
    'scripts/fetch_070_from_n8n.py'
]

base_dir = r'd:\AntiGravity\projeto_01'

for script in scripts:
    path = os.path.join(base_dir, script)
    if not os.path.exists(path):
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    warning = '"""\n[DEPRECATED] Manus.IA removido do ecossistema DL Nexus.\nEste script foi desativado.\n"""\nimport sys\nsys.exit("Script obsoleto. Manus.IA foi removido.")\n\n'
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(warning + content)
        
    print(f'Deprecated {script}')
