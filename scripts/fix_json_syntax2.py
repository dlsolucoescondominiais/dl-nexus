import glob
import os

folder = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\SOCIAL_GERADOR_REVISOR_DL.json'
target_str = '"url": "=https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key=" + process.env.GEMINI_API_KEY_MOTOR'
replacement_str = '"url": "={{ \'https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key=\' + $env.GEMINI_API_KEY_MOTOR }}"'

for path in glob.glob(folder):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if target_str in content:
        content = content.replace(target_str, replacement_str)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {os.path.basename(path)}")
