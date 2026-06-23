import json

# Mock Data Provided by User
mock_post = {
    "produto_dl": "DL Guardião",
    "publico_alvo": "Síndicos e administradoras",
    "tema": "CFTV em condomínios",
    "legenda_facebook": "A segurança do seu condomínio é prioridade. Agende uma Avaliação Técnica hoje mesmo!",
    "legenda_instagram": "Proteja seu patrimônio com CFTV avançado. Solicite Avaliação Técnica!",
    "image_url": "https://dlsolucoescondominiais.com.br/assets/controle_acesso.png",
    "status_killcritic": "APROVADO",
    "dry_run": True
}

# Emulate N8N Evaluation
def evaluate_killcritic(status):
    return status == "APROVADO"

def evaluate_dry_run(dry_run):
    return dry_run == True

def generate_facebook_payload(post_data):
    if evaluate_dry_run(post_data['dry_run']):
        return "BLOCKED_BY_DRY_RUN", None
    
    if post_data.get('image_url'):
        return "/photos", {"message": post_data['legenda_facebook'], "url": post_data['image_url']}
    else:
        return "/feed", {"message": post_data['legenda_facebook']}

def generate_instagram_payload(post_data):
    if evaluate_dry_run(post_data['dry_run']):
        return "BLOCKED_BY_DRY_RUN", None
    
    if not post_data.get('image_url'):
        return "pendente_imagem", None
        
    media_payload = {"caption": post_data['legenda_instagram'], "image_url": post_data['image_url']}
    publish_payload = {"creation_id": "<MOCK_CREATION_ID>"}
    
    return "/media and /media_publish (Wait 10s)", {"media": media_payload, "publish": publish_payload}

def emulate_supabase_log(post_data):
    # If dry run is active, the node sets specific values
    if evaluate_dry_run(post_data['dry_run']):
        return {
            "status_facebook": "dry_run_ok",
            "status_instagram": "dry_run_ok",
            "erros.facebook": {},
            "erros.instagram": {},
            "tentativas.facebook": 1,
            "tentativas.instagram": 1,
            "publicado_em.facebook": "<ISO_DATE>",
            "publicado_em.instagram": "<ISO_DATE>",
            "dry_run": True
        }
    return {}

# Run Validations
killcritic_passed = evaluate_killcritic(mock_post['status_killcritic'])
dry_run_passed = evaluate_dry_run(mock_post['dry_run'])

fb_endpoint, fb_payload = generate_facebook_payload(mock_post)
ig_endpoint, ig_payload = generate_instagram_payload(mock_post)

# Print results to console
print("KILLCRITIC Validated:", killcritic_passed)
print("DRY_RUN Validated:", dry_run_passed)
print("Facebook Payload Generation Blocks Correctly:", fb_endpoint == "BLOCKED_BY_DRY_RUN")
print("Instagram Payload Generation Blocks Correctly:", ig_endpoint == "BLOCKED_BY_DRY_RUN")

# To test actual payload generation, temporarily disable dry run
mock_post['dry_run'] = False
fb_end_real, fb_pay_real = generate_facebook_payload(mock_post)
ig_end_real, ig_pay_real = generate_instagram_payload(mock_post)

print(f"Facebook Endpoint: {fb_end_real}")
print(f"Facebook Payload: {fb_pay_real}")
print(f"Instagram Endpoint: {ig_end_real}")
print(f"Instagram Payload: {ig_pay_real}")
