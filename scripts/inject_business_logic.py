import json
import glob
import os

folder = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\*.json'

FB_PAGE_ID_EXP = "{{$env.FACEBOOK_PAGE_ID || '100063696635033'}}"
IG_BIZ_ID_EXP = "{{$env.INSTAGRAM_BUSINESS_ACCOUNT_ID || '3136866194'}}"

def process_file(filepath):
    changed = False
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        return False
        
    for node in data.get('nodes', []):
        node_name = node.get('name', '')
        
        # 1. Instagram Container
        if 'Instagram Container' in node_name or 'Criar Container de Mídia' in node_name:
            if node['type'] == 'n8n-nodes-base.httpRequest':
                params = node.get('parameters', {})
                params['url'] = f"=https://graph.facebook.com/v25.0/{IG_BIZ_ID_EXP}/media"
                
                # Check JSON body logic
                # Ensure it creates media container correctly
                params['jsonBody'] = "={\n  \"caption\": \"{{$json.legenda_instagram}}\",\n  \"image_url\": \"{{$json.image_url}}\"\n}"
                node['parameters'] = params
                changed = True
                
        # 2. Instagram Publish Container
        if 'Instagram Publish' in node_name or 'Publicar no Instagram' in node_name:
            if node['type'] == 'n8n-nodes-base.httpRequest':
                params = node.get('parameters', {})
                params['url'] = f"=https://graph.facebook.com/v25.0/{IG_BIZ_ID_EXP}/media_publish"
                changed = True
                
        # 3. Wait node for 10s
        if 'Aguardar' in node_name and node.get('type') == 'n8n-nodes-base.wait':
            params = node.get('parameters', {})
            if params.get('amount') == 5:
                params['amount'] = 10
                node['parameters'] = params
                changed = True

        # 4. Facebook Publish node
        if 'Facebook Publish' in node_name or 'Facebook Page Feed' in node_name or 'Facebook /photos' in node_name or 'Facebook /feed' in node_name:
            if node['type'] == 'n8n-nodes-base.httpRequest':
                params = node.get('parameters', {})
                # Dynamic URL based on image_url
                params['url'] = f"={{{{ $json.image_url ? 'https://graph.facebook.com/v25.0/' + ($env.FACEBOOK_PAGE_ID || '100063696635033') + '/photos' : 'https://graph.facebook.com/v25.0/' + ($env.FACEBOOK_PAGE_ID || '100063696635033') + '/feed' }}}}"
                
                # Dynamic JSON body based on image_url
                # For /photos: requires url + message
                # For /feed: requires only message
                js_body = """={
  "message": "{{$json.legenda_facebook}}"
  {{ $json.image_url ? ',"url": "' + $json.image_url + '"' : '' }}
}"""
                params['jsonBody'] = js_body
                node['parameters'] = params
                changed = True
                
        # 5. Token Verifier
        if 'Verificar Token Meta' in node_name:
            params = node.get('parameters', {})
            params['url'] = f"=https://graph.facebook.com/v25.0/{FB_PAGE_ID_EXP}?fields=id,name,username,link,instagram_business_account"
            
            # appsecret_proof support
            qs = """={
  "appsecret_proof": "{{ $env.META_APP_SECRET ? $evaluateExpression('crypto.createHmac(\\'sha256\\', $env.META_APP_SECRET).update($env.META_TOKEN).digest(\\'hex\\')') : '' }}"
}"""
            params['sendQuery'] = True
            params['specifyQuery'] = 'json'
            params['jsonQuery'] = qs
            
            node['parameters'] = params
            changed = True
            
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    return changed

count = 0
for path in glob.glob(folder):
    if process_file(path):
        print(f"Updated logic in {os.path.basename(path)}")
        count += 1

print(f"Total files updated: {count}")
