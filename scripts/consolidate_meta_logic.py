import json
import os

# 1. Update SOCIAL_GERADOR_REVISOR_DL.json compliance rules
path_gerador = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\SOCIAL_GERADOR_REVISOR_DL.json'

try:
    with open(path_gerador, 'r', encoding='utf-8') as f:
        gerador_data = json.load(f)
        
    for node in gerador_data.get('nodes', []):
        if node.get('name') == 'Gerar Copys (Gemini)':
            body = node['parameters'].get('jsonBody', '')
            
            # Append new rules to prompt if not exists
            if 'urgente demais' not in body:
                new_rules = """
- NUNCA use o termo 'visita técnica'. Use SEMPRE 'Avaliação Técnica'.
- NUNCA use 'Condfy'.
- NUNCA use 'DL Ignis'. Use 'DL Alerta' com a expressão 'prevenção de incêndio'.
- NUNCA chame o Diogo de 'engenheiro'.
- NUNCA cite a palavra 'B2B' ou 'n8n', 'webhook', 'payload', 'API', 'CRM' em texto público.
- NUNCA garanta 'preço final', 'garantia eterna', '100% garantido', 'sem risco', 'última chance', 'urgente demais'.
- NÃO trate Mult Grill como produto próprio; use 'DL Express' para suporte técnico de Mult Grill.
"""
                body = body.replace('- NUNCA use o termo \\\'visita técnica\\\'.', new_rules)
                node['parameters']['jsonBody'] = body
                
    with open(path_gerador, 'w', encoding='utf-8') as f:
        json.dump(gerador_data, f, indent=2, ensure_ascii=False)
except Exception as e:
    print("Error updating Gerador:", e)

# 2. Emulate the 2 Tests required
def simulate_publishing(mock):
    fb_endpoint = ""
    fb_payload = {}
    ig_endpoint = ""
    ig_payload = {}
    
    # 1. Check DRY_RUN
    if mock['dry_run']:
        print(f"--- TESTE DRY RUN (image_url={'VAZIO' if not mock['image_url'] else 'VALIDO'}) ---")
        # 2. Check KILLCRITIC
        if mock['status_killcritic'] != 'APROVADO':
            print("KILLCRITIC BLOQUEOU")
            return
            
        # 3. Facebook Branch
        if mock['image_url']:
            fb_endpoint = "/photos"
            fb_payload = {"message": mock['legenda_facebook'], "url": mock['image_url']}
        else:
            fb_endpoint = "/feed"
            fb_payload = {"message": mock['legenda_facebook']}
            
        # 4. Instagram Branch
        if not mock['image_url']:
            ig_endpoint = "SKIPPED"
            ig_payload = {"status": "pendente_imagem"}
        else:
            ig_endpoint = "/media -> wait 10s -> /media_publish"
            ig_payload = {"caption": mock['legenda_instagram'], "image_url": mock['image_url']}
            
        print(f"FB Endpoint: {fb_endpoint}")
        print(f"FB Payload: {fb_payload}")
        print(f"IG Endpoint: {ig_endpoint}")
        print(f"IG Payload: {ig_payload}")
        print("Log Supabase Simulados: status_facebook='dry_run_ok', status_instagram='dry_run_ok' ou 'pendente_imagem'")
        print("--------------------------------------------------\n")

# Test 1: Empty image_url
mock_1 = {
    "produto_dl": "DL Guardião",
    "tema": "CFTV em condomínios",
    "publico_alvo": "Síndicos e administradoras",
    "legenda_facebook": "Texto institucional com CTA para Avaliação Técnica.",
    "legenda_instagram": "Texto curto com CTA para Avaliação Técnica.",
    "image_url": "",
    "status_killcritic": "APROVADO",
    "dry_run": True
}

# Test 2: Valid image_url
mock_2 = {
    "produto_dl": "DL Guardião",
    "tema": "CFTV em condomínios",
    "publico_alvo": "Síndicos e administradoras",
    "legenda_facebook": "Texto institucional com CTA para Avaliação Técnica.",
    "legenda_instagram": "Texto curto com CTA para Avaliação Técnica.",
    "image_url": "https://dlsolucoescondominiais.com.br/assets/cftv.jpg",
    "status_killcritic": "APROVADO",
    "dry_run": True
}

simulate_publishing(mock_1)
simulate_publishing(mock_2)
