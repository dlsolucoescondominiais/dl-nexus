import os
import requests
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import PlainTextResponse

META_VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")
if not META_VERIFY_TOKEN:
    raise RuntimeError("META_VERIFY_TOKEN ausente. Configure no .env")

N8N_WEBHOOK_META = os.getenv("N8N_WEBHOOK_META")
if not N8N_WEBHOOK_META:
    raise RuntimeError("N8N_WEBHOOK_META ausente. Configure no .env (ex: http://n8n:5678/webhook/dl-receptor)")

N8N_API_KEY = os.getenv("N8N_API_KEY")
if not N8N_API_KEY:
    raise RuntimeError("N8N_API_KEY ausente. Configure no .env")

router = APIRouter(prefix="/api/meta", tags=["META", "WHATSAPP"])

@router.get("/webhook")
def verify_webhook(request: Request):
    """
    Endpoint para verificação de Webhook do Facebook/Meta.
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == META_VERIFY_TOKEN:
            return PlainTextResponse(content=challenge, status_code=200)
        else:
            raise HTTPException(status_code=403, detail="Verification token mismatch")

    raise HTTPException(status_code=400, detail="Bad Request")

@router.post("/webhook")
def receive_webhook(payload: dict):
    """
    Recebe as mensagens do Meta e repassa para o n8n usando a rede interna e autenticação via header.
    Utiliza def normal (não async) conforme regra de otimização de performance para I/O bloqueante com a lib requests.
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "X-DL-API-KEY": N8N_API_KEY
        }
        # Repassa o JSON inteiro que o Meta enviou para o webhook do Orquestrador
        resp = requests.post(N8N_WEBHOOK_META, json=payload, headers=headers, timeout=10)

        if resp.status_code not in (200, 201):
            print(f"Erro ao encaminhar para N8N: HTTP {resp.status_code} - {resp.text}")

        return {"status": "success"}
    except Exception as e:
        print(f"Falha na integração com N8N: {e}")
        # Mesmo falhando o repasse interno, o Meta espera um 200 OK imediato
        # para parar de reenviar a mensagem.
        return {"status": "error_forwarding", "detail": str(e)}
