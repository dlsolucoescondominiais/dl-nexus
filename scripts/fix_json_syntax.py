import glob
import os

folder = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\*.json'
target_str = '"value": "=Bearer " + process.env.META_TOKEN'
replacement_str = '"value": "={{ \'Bearer \' + $env.META_TOKEN }}"'

for path in glob.glob(folder):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if target_str in content:
        content = content.replace(target_str, replacement_str)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {os.path.basename(path)}")
