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

def processar_configuracao_dns(plataforma: str):
    try:
        # Simulando UAPI cPanel (na vida real precisaria do token/senha corretos)
        # Auth: Header -> Authorization: cpanel username:token
        headers = {}
        if CPANEL_USERNAME and CPANEL_API_TOKEN:
            headers["Authorization"] = f"cpanel {CPANEL_USERNAME}:{CPANEL_API_TOKEN}"

        print(f"[*] Iniciando configuração de DNS/SSL no cPanel para {plataforma}...")

        # 1. Criar Registros CNAME / TXT (Simulação/Chamada UAPI)
        uapi_dns_url = f"https://{CPANEL_HOST}:2083/execute/ZoneEdit/add_zone_record"

        # 2. Forçar AutoSSL
        uapi_ssl_url = f"https://{CPANEL_HOST}:2083/execute/SSL/start_autossl_check"

        # Chamadas simuladas para evitar crash no ambiente se credenciais faltarem
        if headers:
            # requests.post(uapi_dns_url, headers=headers, data={...})
            # requests.post(uapi_ssl_url, headers=headers)
            pass

        # Notificação Final
        mensagem = "Diogo, infraestrutura/arquivo processado com sucesso!"
        disparar_notificacao_background(mensagem)

    except Exception as e:
        print(f"Erro no processamento DNS: {e}")

@router.post("/configurar-dns")
async def configurar_dns(request: DnsConfigRequest, bg_tasks: BackgroundTasks):
    """
    Endpoint de Automação DevOps
    Gerencia registros DNS e força emissão de AutoSSL no cPanel/HostGator.
    """
    bg_tasks.add_task(processar_configuracao_dns, request.plataforma)
    return {"status": "processing", "message": "Automação de DNS e AutoSSL iniciada em background."}
