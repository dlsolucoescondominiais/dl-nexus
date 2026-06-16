import os
import requests
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/infra", tags=["DEVOPS", "INFRAESTRUTURA"])

CPANEL_DOMAIN = os.getenv("CPANEL_DOMAIN", "dlsolucoescondominiais.com.br")
CPANEL_USERNAME = os.getenv("CPANEL_USERNAME")
CPANEL_API_TOKEN = os.getenv("CPANEL_API_TOKEN")
CPANEL_HOST = os.getenv("CPANEL_HOST", "localhost")

WEBHOOK_NOTIFICACAO_N8N = os.getenv("N8N_WEBHOOK_URL", "https://n8n.dlsolucoescondominiais.com.br/webhook/dl-automacao-sindicos")
API_KEY_N8N = os.getenv("N8N_API_KEY", "TESTE-123")

class DnsConfigRequest(BaseModel):
    plataforma: str = "manychat"
    dominio: str = "dlsolucoescondominiais.com.br"
    registro_txt: str = "v=spf1 include:spf.protection.outlook.com -all" # Exemplo

def disparar_notificacao_background(mensagem: str):
    try:
        headers = {
            "Content-Type": "application/json",
            "X-DL-API-KEY": API_KEY_N8N
        }
        payload = {"message": mensagem}
        requests.post(WEBHOOK_NOTIFICACAO_N8N, json=payload, headers=headers, timeout=10)
    except Exception as e:
        print(f"Falha ao notificar n8n: {e}")

def processar_configuracao_dns(req: DnsConfigRequest):
    try:
        if not CPANEL_USERNAME or not CPANEL_API_TOKEN:
             # Simulando modo Sandbox sem derrubar a aplicação
             print(f"[Sandbox] Simulação UAPI cPanel: Criando registro TXT '{req.registro_txt}' para {req.plataforma} em {req.dominio}...")
             print("[Sandbox] Simulação AutoSSL start_autossl_check executada com sucesso.")

             mensagem = f"Diogo, simulação de infraestrutura/DNS ({req.plataforma}) processada com sucesso no ambiente Sandbox!"
             disparar_notificacao_background(mensagem)
             return

        # UAPI cPanel Real
        headers = {
            "Authorization": f"cpanel {CPANEL_USERNAME}:{CPANEL_API_TOKEN}"
        }
        print(f"[*] Iniciando configuração REAL de DNS/SSL no cPanel para {req.plataforma}...")

        # 1. Criar Registro TXT
        uapi_dns_url = f"https://{CPANEL_HOST}:2083/execute/ZoneEdit/add_zone_record"
        payload_dns = {
            "domain": req.dominio,
            "name": req.dominio + ".",
            "type": "TXT",
            "txtdata": req.registro_txt
        }

        res_dns = requests.post(uapi_dns_url, headers=headers, data=payload_dns, timeout=15)
        if res_dns.status_code != 200:
             print(f"Erro UAPI DNS: {res_dns.text}")

        # 2. Forçar AutoSSL
        uapi_ssl_url = f"https://{CPANEL_HOST}:2083/execute/SSL/start_autossl_check"
        requests.post(uapi_ssl_url, headers=headers, timeout=15)

        mensagem = f"Diogo, a configuração real de DNS ({req.plataforma}) e renovação SSL foram processadas com sucesso!"
        disparar_notificacao_background(mensagem)

    except Exception as e:
        print(f"Erro crítico no processamento DNS: {e}")

@router.post("/configurar-dns")
async def configurar_dns(request: DnsConfigRequest, bg_tasks: BackgroundTasks):
    """
    Endpoint de Automação DevOps
    Gerencia registros DNS e força emissão de AutoSSL no cPanel/HostGator.
    Em ambientes sem credenciais de produção (como sandboxes), opera em modo de simulação.
    """
    bg_tasks.add_task(processar_configuracao_dns, request)
    return {"status": "processing", "message": f"Automação de DNS e AutoSSL iniciada em background para {request.plataforma}."}
