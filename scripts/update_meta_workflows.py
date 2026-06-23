import json
import glob
import os
import re

FOLDER = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS'

# FB/IG constants
FB_PAGE_ID = '100063696635033'
IG_BIZ_ID = '3136866194'

ENV_FB = "{{$env.FACEBOOK_PAGE_ID || '" + FB_PAGE_ID + "'}}"
ENV_IG = "{{$env.INSTAGRAM_BUSINESS_ACCOUNT_ID || '" + IG_BIZ_ID + "'}}"

def clean_json_string(s):
    # This is a naive heuristic to fix unescaped double quotes inside values if they broke the json
    # A safer approach is just to ignore completely broken JSON and report it, or try to fix known n8n export bugs.
    # N8n exports are usually valid JSON. Let's just try to fix trailing commas and missing commas.
    s = re.sub(r',\s*\}', '}', s)
    s = re.sub(r',\s*\]', ']', s)
    return s

def process_workflow(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Read error: {e}"

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        # Try to fix
        content = clean_json_string(content)
        try:
            data = json.loads(content)
        except Exception as e2:
            return False, f"JSON Error: {e}"

    changed = False
    nodes = data.get('nodes', [])

    # Apply changes
    for node in nodes:
        node_str = json.dumps(node, ensure_ascii=False)
        
        # 1. Replace placeholders globally in this node
        if 'PAGE_ID_AQUI' in node_str or 'INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI' in node_str or FB_PAGE_ID in node_str or IG_BIZ_ID in node_str:
            # We don't want to replace if it's already the env var. So replace literal IDs and placeholders to env var.
            # But only if it's not already env var
            params = node.get('parameters', {})
            for k, v in params.items():
                if isinstance(v, str):
                    if 'PAGE_ID_AQUI' in v:
                        params[k] = v.replace('PAGE_ID_AQUI', ENV_FB)
                        changed = True
                    if FB_PAGE_ID in v and ENV_FB not in v:
                        params[k] = v.replace(FB_PAGE_ID, ENV_FB)
                        changed = True
                        
                    if 'INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI' in v:
                        params[k] = v.replace('INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI', ENV_IG)
                        changed = True
                    if IG_BIZ_ID in v and ENV_IG not in v:
                        params[k] = v.replace(IG_BIZ_ID, ENV_IG)
                        changed = True

        # 2. Fix Endpoints
        # Facebook
        if node.get('type') == 'n8n-nodes-base.httpRequest':
            url = node.get('parameters', {}).get('url', '')
            if 'graph.facebook.com' in url:
                # Check FB endpoints
                if FB_PAGE_ID in url or 'FACEBOOK_PAGE_ID' in url:
                    # Update to v25.0
                    node['parameters']['url'] = url.replace('v20.0', 'v25.0').replace('v19.0', 'v25.0')
                    # Condition for /photos vs /feed will be handled in the workflow logic itself, 
                    # but if it's a static URL, we ensure it's v25.0. 
                    # If user asked to "usar /photos com url e message", usually it's an expression.
                    changed = True
                
                # Check IG endpoints
                if IG_BIZ_ID in url or 'INSTAGRAM_BUSINESS_ACCOUNT_ID' in url:
                    node['parameters']['url'] = url.replace('v20.0', 'v25.0').replace('v19.0', 'v25.0')
                    changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True, "Updated successfully"
    return False, "No changes needed"

# Process all JSONs
files = glob.glob(os.path.join(FOLDER, '*.json'))
report = []
for f in files:
    filename = os.path.basename(f)
    if 'SOCIAL' in filename or 'PUBLICADOR' in filename or '020' in filename or '081' in filename or '082' in filename:
        success, msg = process_workflow(f)
        report.append(f"{filename}: {msg}")

with open(r'd:\AntiGravity\projeto_01\scripts\meta_update_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))
