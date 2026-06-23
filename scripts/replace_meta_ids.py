import os
import json

directory = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS"
target_files = [
    "SOCIAL_PUBLICADOR_MULTICANAL_DL.json",
    "020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json",
    "SOCIAL_VERIFICADOR_TOKEN_META.json",
    "081_PUBLICADOR_INSTAGRAM_META_API.json",
    "082_PUBLICADOR_FACEBOOK_META_API.json"
]

old_fb = "100063696635033"
new_fb = "100166804716824"
old_ig = "3136866194"
new_ig = "17841403185822108"

for filename in target_files:
    filepath = os.path.join(directory, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated_content = content.replace(old_fb, new_fb).replace(old_ig, new_ig)
        
        if updated_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated: {filename}")
        else:
            print(f"No changes needed: {filename}")
    else:
        print(f"File not found: {filename}")
